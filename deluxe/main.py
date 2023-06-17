import random

from mongoengine import connect

import modern
from deluxe.bot import bot
from deluxe.game.Entities.Cow import Cow
from deluxe.game.matchmaking.Matchmaker import Matchmaker
from deluxe.db.Rating import RatingManager
from config import admin, mongourl

from game.ContentManager import ContentManager

mm = Matchmaker(bot)
rm = RatingManager()
cm = ContentManager()
connect(host=mongourl, db='viro')


@bot.message_handler(func=lambda m: rm.process_lambda(m))
def start_handler(m):
    pass


@bot.message_handler(commands=['top'])
def h(m):
    tts = rm.get_top()
    bot.reply_to(m, tts)


@bot.message_handler(commands=['bk'])
def h(m):
    rm.get_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
    if m.text.count(' ') != 2:
        return
    _, a, b = m.text.split(' ')
    a, b = rm.get_by_username(a), rm.get_by_username(b)
    if not (a and b):
        bot.reply_to(m, 'Нет!!!')
        return
    EWP_a = 1 / (1 + (10 ** ((b.rating - a.rating) / 400)))
    EWP_b = 1 / (1 + (10 ** ((a.rating - b.rating) / 400)))
    C_a = round(1/EWP_a, 2)
    C_b = round(1/EWP_b, 2)
    bot.reply_to(m, f'{a.name} {C_a} | {C_b} {b.name}')


@bot.message_handler(commands=['predict'])
def h(m):
    rm.get_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
    if m.text.count(' ') != 4:
        return
    _, a, b, a_s, b_s = m.text.split(' ')
    a_s, b_s = int(a_s), int(b_s)
    a, b = rm.get_by_username(a), rm.get_by_username(b)
    if not (a and b):
        bot.reply_to(m, 'Нет!!!')
        return
    r_a, r_b = rm.outcome(a, b, a_s, b_s)
    a_emoji = '📈' if r_a > a.rating else '📉'
    b_emoji = '📈' if r_b > b.rating else '📉'
    bot.reply_to(m, f'ПРОГНОЗ:\n\nБой: {a.name} ({a.rating}) vs {b.name} ({b.rating}): {a_s} - {b_s}\n\n'
                    f'Результат: \n'
                    f'{a.name} - {r_a}{a_emoji} \n'
                    f'{b.name} - {r_b}{b_emoji}')


@bot.message_handler(commands=['vs'])
def h(m):
    rm.get_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
    if m.from_user.id != admin:
        return
    if m.text.count(' ') != 4:
        return
    _, a, b, a_s, b_s = m.text.split(' ')
    a_s, b_s = int(a_s), int(b_s)
    a, b = rm.get_by_username(a), rm.get_by_username(b)
    if not (a and b):
        bot.reply_to(m, 'Нет!!!')
        return
    r_a, r_b = rm.outcome(a, b, a_s, b_s)
    a_emoji = '📈' if r_a > a.rating else '📉'
    b_emoji = '📈' if r_b > b.rating else '📉'
    bot.reply_to(m, f'Бой: {a.name} ({a.rating}) vs {b.name} ({b.rating}): {a_s} - {b_s}\n\n'
                    f'Результат: \n'
                    f'{a.name} - {r_a}{a_emoji} \n'
                    f'{b.name} - {r_b}{b_emoji}')
    a.rating = int(r_a)
    b.rating = int(r_b)
    a.save(), b.save()


@bot.message_handler(commands=['vd_prepare'])
def vd_prepare_handler(m):
    game = mm.get_game(m.chat.id)
    if game:
        bot.reply_to(m, 'Игра уже запущена! Вступайте командой /vd_join.')
        return
    mm.create_game(m.chat.id)
    bot.reply_to(m, 'Набор в игру запущен! Заходите командой /vd_join.')


@bot.message_handler(commands=['vd_go'])
def vd_join_handler(m):
    game = mm.get_game(m.chat.id)
    if not game:
        bot.reply_to(m, 'Игра не запущена! Запустите командой /vd_prepare.')
        return
    if m.from_user.id not in game.player_ids:
        bot.reply_to(m, 'Вас нет в игре, не вам и запускать!')
        return
    if not game.lobby:
        bot.reply_to(m, 'Игра уже идет!')
        return
    game.lobby = False
    mm.choose_items(m.chat.id)
    mm.choose_weapons(m.chat.id)
    bot.reply_to(m, 'Игра начинается!')


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


@bot.message_handler(commands=['add_cow'])
def vd_join_handler(m):
    game = mm.get_game(m.chat.id)
    if not m.text.count(' ') or not m.text.split(' ')[1].isdigit():
        bot.reply_to(m, 'Так нельзя. Напиши /add_cow число.')
        return
    count = int(m.text.split(' ')[1])
    if not (0 < count < 15):
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
    if weapon_id == 'random':
        weapon = random.choice(modern.all_weapons)(player)
    else:
        weapon = mm.get_weapon(int(weapon_id), player)
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
    skill = mm.get_skill(skill_id, player)
    player.skills.append(skill)

    if int(cycle) >= game.skill_cycles:
        player.chose_skills = True
    else:
        mm.send_skill_choice_buttons(player, game.skill_number, int(cycle)+1)

    bot.edit_message_text(f'Выбран скилл: {skill.name}', c.message.chat.id, c.message.message_id)

    if not game.not_chosen_skills:
        tts = f'Способности выбраны, игра начинается! Выбор оружия:'
        for player in game.alive_entities:
            tts += f'\n{player.name}: {player.weapon.name}'
        bot.send_message(game.chat_id, tts)
        mm.pre_move(game.chat_id)


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
        item = player.action_queue[index]
    item.target = target

    bot.edit_message_text(f'Выбрано: {item.name} на {item.target.name}',
                          c.message.chat.id, c.message.message_id)

    if item.cost < 1:
        if item.cost == -1:
            item()
            player.item_queue.remove(item)
            player.update_actions()
        mm.send_act_buttons(player, game)
        return

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
