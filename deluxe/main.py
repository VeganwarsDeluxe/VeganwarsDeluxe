import random
import traceback

from telebot import types

import modern
from config import admin
from deluxe.bot import bot, mm, cm
from deluxe.game.Entities.Cow import Cow


#       Handler imports


@bot.message_handler(commands=['do'])
def vd_prepare_handler(m):
    if m.from_user.id != admin:
        return
    if not m.text.count(' '):
        return
    code = m.text.split(' ', 1)[1]
    try:
        result = eval(code)
    except:
        result = traceback.format_exc()
    bot.reply_to(m, f"Code: {code}\n\nResult: {result}")


@bot.message_handler(commands=['vd_prepare'])
def vd_prepare_handler(m):
    game = mm.get_game(m.chat.id)

    if game:
        if game.lobby:
            bot.reply_to(game.lobby_message, 'Игра уже запущена!')
        else:
            bot.reply_to(m, 'Игра уже идет!')
        return

    game = mm.create_game(m.chat.id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='♿️Вступить в игру', url=bot.get_deep_link(f"jg_{m.chat.id}")))
    kb.add(types.InlineKeyboardButton(text='▶️Запустить игру', callback_data="vd_go"))
    m = bot.send_message(m.chat.id, f'Игра: {game.name}\n\nУчастники:', reply_markup=kb)
    game.lobby_message = m


@bot.message_handler(commands=['vd_delete'])
def vd_prepare_handler(m):
    game = mm.get_game(m.chat.id)
    if not game:
        bot.reply_to(m, 'Игра и так не запущена!')
        return
    mm.create_game(m.chat.id)
    del mm.games[m.chat.id]
    bot.reply_to(m, 'Игра удалена.')


@bot.message_handler(commands=['start'], func=lambda m: " jg_" in m.text)
def vd_prepare_handler(m):
    game_id = int(m.text.split('_')[-1])
    game = mm.get_game(game_id)
    if not game:
        bot.reply_to(m, 'Данная игра не запущена!')
        return
    if m.from_user.id in game.player_ids:
        bot.reply_to(m, 'Вы уже в игре!')
        return
    if not game.lobby:
        bot.reply_to(m, 'Игра уже идет!')
        return
    bot.send_message(m.from_user.id, 'Вы вступили в игру! Осторжно, бот в бета тесте!')
    bot.send_message(game_id, f'{m.from_user.full_name} вступил в игру!')
    mm.join_game(game_id, m.from_user.id, m.from_user.full_name)


@bot.message_handler(commands=['vd_go'])
def vd_join_handler(m):
    game = mm.get_game(m.chat.id)
    if not game:
        bot.reply_to(m, 'Игра не запущена! Запустите командой /vd_prepare.')
        return
    if m.from_user.id not in game.player_ids:
        if m.from_user.id != admin:
            bot.reply_to(m, 'Вас нет в игре, не вам и запускать!')
            return
    if not game.lobby:
        bot.reply_to(m, 'Игра уже идет!')
        return
    game.lobby = False
    mm.choose_items(m.chat.id)
    mm.choose_weapons(m.chat.id)
    bot.reply_to(m, 'Игра начинается!')


@bot.callback_query_handler(func=lambda c: c.data == 'vd_go')
def act_callback_handler(c):
    game = mm.get_game(c.message.chat.id)
    if not game:
        bot.answer_callback_query(c.id, "Игра не запущена!")
        return
    if c.from_user.id not in game.player_ids:
        if c.from_user.id != admin:
            bot.answer_callback_query(c.id, "Вас нет в игре!")
            return
    if not game.lobby:
        bot.answer_callback_query(c.id, "Игра уже идет!")
        return
    game.lobby = False
    mm.choose_items(c.message.chat.id)
    mm.choose_weapons(c.message.chat.id)
    bot.reply_to(c.message, 'Игра начинается!')


@bot.message_handler(commands=['vd_join'])
def vd_join_handler(m):
    game = mm.get_game(m.chat.id)
    if not game:
        bot.reply_to(m, 'Игра не запущена! Запустите командой /vd_prepare.')
        return
    if m.from_user.id in game.player_ids:
        bot.reply_to(m, 'Вы уже в игре!')
        return
    if not game.lobby:
        bot.reply_to(m, 'Игра уже идет!')
        return
    try:
        bot.send_message(m.from_user.id, 'Вы вступили в игру! Осторжно, бот в бета тесте!')
    except:
        bot.reply_to(m, 'Сначала напишите мне в ЛС!')
        return
    bot.send_message(m.chat.id, f'{m.from_user.full_name} вступил в игру!')
    mm.join_game(m.chat.id, m.from_user.id, m.from_user.full_name)


@bot.message_handler(commands=['vd_suicide'])
def vd_join_handler(m):
    game = mm.get_game(m.chat.id)
    if not game:
        return
    player = game.get_player(m.from_user.id)
    if not player:
        return
    if game.lobby:
        return
    player.hp = -1000
    player.ready = True
    if not game.unready_players:
        game.say(f'☠️|{player.name} совершает суицид.')
        mm.cycle(game)


@bot.message_handler(commands=['add_cow'])
def vd_join_handler(m):
    game = mm.get_game(m.chat.id)
    if not m.text.count(' ') or not m.text.split(' ')[1].isdigit():
        bot.reply_to(m, 'Так нельзя. Напиши /add_cow число.')
        return
    count = int(m.text.split(' ')[1])
    if not (0 <= count <= 15):
        bot.reply_to(m, 'Неправильно. Введи число от 0 до 15')
        return
    if not game:
        bot.reply_to(m, 'Игра не запущена! Запустите командой /vd_prepare.')
        return
    if game.cowed:
        bot.reply_to(m, 'МУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ.')
        return
    game.cowed = True
    for _ in range(count):
        cow = Cow(game)
        game.entities.append(cow)
    mm.update_message(game)
    bot.send_message(m.chat.id, f'{count} коров прибежало!')


@bot.callback_query_handler(func=lambda c: c.data.startswith('cw'))
def act_callback_handler(c):
    _, game_id, weapon_id = c.data.split('_', 2)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра уже закончилась!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Вы не в игре!', c.message.chat.id, c.message.message_id)
        return
    if player.chose_weapon:
        bot.edit_message_text(f'Хватит так поступать.', c.message.chat.id, c.message.message_id)
        return
    if weapon_id == 'random':
        weapon = random.choice(modern.all_weapons)(player)
    else:
        weapon = mm.get_weapon(weapon_id, player)
    player.weapon = weapon
    player.chose_weapon = True
    if not game.not_chosen_weapon:
        bot.send_message(game.chat_id, f'Оружие выбрано.')
        mm.choose_skills(int(game_id))

    bot.edit_message_text(f'Выбрано оружие: {weapon.name}', c.message.chat.id, c.message.message_id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('cs'))
def act_callback_handler(c):
    _, cycle, game_id, skill_id = c.data.split('_', 3)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра уже закончилась!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Вы не в игре!', c.message.chat.id, c.message.message_id)
        return
    if player.chose_skills or player.skill_cycle == int(cycle):
        bot.edit_message_text(f'Хватит так поступать.', c.message.chat.id, c.message.message_id)
        return
    skill = mm.get_skill(skill_id, player)
    player.skills.append(skill)
    player.skill_cycle = int(cycle)

    if int(cycle) >= game.skill_cycles:
        player.chose_skills = True
    else:
        mm.send_skill_choice_buttons(player, game.skill_number, int(cycle) + 1)

    bot.edit_message_text(f'Выбран скилл: {skill.name}', c.message.chat.id, c.message.message_id)

    if not game.not_chosen_skills:
        tts = f'Способности выбраны, игра начинается! Выбор оружия:'
        for player in game.alive_entities:
            tts += f'\n{player.name}: {player.weapon.name}'
        bot.send_message(game.chat_id, tts)
        mm.start_game(game)


@bot.callback_query_handler(func=lambda c: c.data.startswith('ci'))
def act_callback_handler(c):
    _, skill_id = c.data.split('_', 3)
    bot.answer_callback_query(c.id, cm.get_skill(skill_id).description, show_alert=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith('wi'))
def act_callback_handler(c):
    _, weapon_id = c.data.split('_', 3)
    bot.answer_callback_query(c.id, cm.get_weapon(weapon_id).description, show_alert=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith('item_'))
def act_callback_handler(c):
    _, game_id, item_id = c.data.split('_', 2)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    action = player.get_item(item_id)
    if not action:
        bot.edit_message_text('Кнопка стухла!', c.message.chat.id, c.message.message_id)
        return
    if action.blocked:
        bot.answer_callback_query(c.id, "Кнопка заблокирована!", show_alert=True)
        return
    bot.edit_message_text(f"Выбрано: {action.name}", c.message.chat.id, c.message.message_id)
    mm.choose_item(game, c.from_user.id, item_id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('act_'))
def act_callback_handler(c):
    _, game_id, act_id = c.data.split('_', 2)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    action = player.get_action(act_id)
    if not action:
        bot.edit_message_text('Кнопка стухла!', c.message.chat.id, c.message.message_id)
        return
    if action.blocked:
        bot.answer_callback_query(c.id, "Кнопка заблокирована!", show_alert=True)
        return
    bot.edit_message_text(f"Выбрано: {action.name}", c.message.chat.id, c.message.message_id)
    mm.choose_act(game, c.from_user.id, act_id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('back_'))
def act_callback_handler(c):
    _, game_id = c.data.split('_', 1)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    kb = mm.get_act_buttons(player, game)
    tts = mm.get_act_text(player, game)
    bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith('more_'))
def act_callback_handler(c):
    _, game_id = c.data.split('_', 1)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    kb = mm.get_additional_buttons(player, game)
    bot.edit_message_text('Дополнительно:', c.message.chat.id, c.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith('itgt_'))
def act_callback_handler(c):
    _, game_id, target_id, index = c.data.split('_', 3)
    index = int(index)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    target = game.get_player(int(target_id))
    if not target:
        bot.edit_message_text('Цель стухла!', c.message.chat.id, c.message.message_id)
        return

    item = player.action
    if index != -1:
        item = player.item_queue[index]
    item.target = target
    item.canceled = False

    bot.edit_message_text(f'Выбрано: {item.name} на {item.target.name}',
                          c.message.chat.id, c.message.message_id)

    if item.cost < 1:
        mm.send_act_buttons(player, game)
        return

    player.items.remove(item) if item in player.items else bot.send_message(admin, 'Та за шо.')

    player.ready = True
    if not game.unready_players:
        mm.cycle(game)


@bot.callback_query_handler(func=lambda c: c.data.startswith('tgt_'))
def act_callback_handler(c):
    _, game_id, target_id, index = c.data.split('_', 3)
    index = int(index)
    game = mm.get_game(int(game_id))
    if not game:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = game.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    target = game.get_player(int(target_id))
    if not target:
        bot.edit_message_text('Цель стухла!', c.message.chat.id, c.message.message_id)
        return

    action = player.action
    if index != -1:
        action = player.action_queue[index]
    action.target = target
    action.canceled = False

    bot.edit_message_text(f'Выбрано: {action.name} на {target.name}',
                          c.message.chat.id, c.message.message_id)

    if action.cost < 1:
        if action.cost == -1:
            action()
            player.action_queue.remove(action)
            player.update_actions()
        mm.send_act_buttons(player, game)
        return

    player.ready = True
    if not game.unready_players:
        mm.cycle(game)


bot.infinity_polling()
