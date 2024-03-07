import random
import traceback

from telebot import types

#       Handler imports
import deluxe.bot.rating
from VegansDeluxe import rebuild
from config import admin

from VegansDeluxe.core import Own
from deluxe.startup import bot, cm, engine
from deluxe.game.Entities.Cow import Cow
from deluxe.game.Matches.RatFight import RatDungeon

print(deluxe.bot.rating, "loaded.")
from deluxe.game.Matches.BasicMatch import BasicMatch
from deluxe.game.Matches.ElementalDungeon import ElementalDungeon
from deluxe.game.Matches.Matchmaker import Matchmaker
from deluxe.game.Matches.TestGameMatch import TestGameMatch

mm = Matchmaker(bot, engine)


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
    match = mm.get_match(m.chat.id)

    if match:
        if match.lobby and match.lobby_message:
            bot.reply_to(match.lobby_message, 'Игра уже запущена!')
        else:
            bot.reply_to(m, 'Игра уже идет!')
        return

    match = BasicMatch(m.chat.id)
    mm.attach_match(match)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='♿️Вступить в игру', url=bot.get_deep_link(f"jg_{m.chat.id}")))
    kb.add(types.InlineKeyboardButton(text='▶️Запустить игру', callback_data="vd_go"))
    m = bot.send_message(m.chat.id, f'Игра: {match.name}\n\nУчастники:', reply_markup=kb)
    match.lobby_message = m


@bot.message_handler(commands=['vd_testgame'])
def vd_prepare_handler(m):
    match = mm.get_match(m.chat.id)

    if match:
        if match.lobby:
            bot.reply_to(match.lobby_message, 'Игра уже запущена!')
        else:
            bot.reply_to(m, 'Игра уже идет!')
        return

    match = TestGameMatch(m.chat.id)
    mm.attach_match(match)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='♿️Вступить в игру', url=bot.get_deep_link(f"jg_{m.chat.id}")))
    kb.add(types.InlineKeyboardButton(text='▶️Запустить игру', callback_data="vd_go"))
    m = bot.send_message(m.chat.id, f'Игра: {match.name}\n\nУчастники:', reply_markup=kb)
    match.lobby_message = m


@bot.message_handler(commands=['vd_rats'])
def vd_prepare_handler(m):
    match = mm.get_match(m.chat.id)

    if match:
        if match.lobby:
            bot.reply_to(match.lobby_message, 'Игра уже запущена!')
        else:
            bot.reply_to(m, 'Игра уже идет!')
        return

    match = RatDungeon(m.chat.id)
    mm.attach_match(match)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='♿️Вступить в игру', url=bot.get_deep_link(f"jg_{m.chat.id}")))
    kb.add(types.InlineKeyboardButton(text='▶️Запустить игру', callback_data="vd_go"))
    m = bot.send_message(m.chat.id, f'Игра: {match.name}\n\nУчастники:', reply_markup=kb)
    match.lobby_message = m


@bot.message_handler(commands=['vd_elemental'])
def vd_prepare_handler(m):
    match = mm.get_match(m.chat.id)

    if match:
        if match.lobby:
            bot.reply_to(match.lobby_message, 'Игра уже запущена!')
        else:
            bot.reply_to(m, 'Игра уже идет!')
        return

    match = ElementalDungeon(m.chat.id)
    mm.attach_match(match)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='♿️Вступить в игру', url=bot.get_deep_link(f"jg_{m.chat.id}")))
    kb.add(types.InlineKeyboardButton(text='▶️Запустить игру', callback_data="vd_go"))
    m = bot.send_message(m.chat.id, f'Игра: {match.name}\n\nУчастники:', reply_markup=kb)
    match.lobby_message = m


@bot.message_handler(commands=['vd_rebuild_collection'])
def vd_prepare_handler(m):
    if True:
        return

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Обычная', callback_data="kek"),
           types.InlineKeyboardButton(text='Обычная командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Рандомная', callback_data="kek"),
           types.InlineKeyboardButton(text='Рандомная командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Тестовая', callback_data="kek"),
           types.InlineKeyboardButton(text='Тестовая командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Рапирная', callback_data="kek"),
           types.InlineKeyboardButton(text='Рапирная командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Битва против крыс', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Битва боссов', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Носорог', callback_data="kek"),
           types.InlineKeyboardButton(text='Вурдалаки', callback_data="kek"),
           types.InlineKeyboardButton(text='Тьма', callback_data="kek"))
    bot.send_message(m.chat.id, f'Коллекция: Rebuild Edition\n\nВыбор игры:', reply_markup=kb)


@bot.message_handler(commands=['vd_classic_collection'])
def vd_prepare_handler(m):
    if True:
        return

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Обычная', callback_data="kek"),
           types.InlineKeyboardButton(text='Обычная командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Рандомная', callback_data="kek"),
           types.InlineKeyboardButton(text='Рандомная командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Тестовая', callback_data="kek"),
           types.InlineKeyboardButton(text='Тестовая командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Кастомная', callback_data="kek"),
           types.InlineKeyboardButton(text='Кастомная командная', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Битва против крыс', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Битва против волков', callback_data="kek"))
    kb.add(types.InlineKeyboardButton(text='Битва с носорогом', callback_data="kek"))
    bot.send_message(m.chat.id, f'Коллекция: Classic Edition\n\nВыбор игры:', reply_markup=kb)


@bot.message_handler(commands=['vd_delete'])
def vd_prepare_handler(m):
    match = mm.get_match(m.chat.id)
    if not match:
        bot.reply_to(m, 'Игра и так не запущена!')
        return
    del mm.matches[match.id]
    engine.session_manager.delete_session(match.session.id)
    bot.reply_to(m, 'Игра удалена.')


@bot.message_handler(commands=['start'], func=lambda m: " jg_" in m.text)
def vd_prepare_handler(m):
    game_id = int(m.text.split('_')[-1])
    match = mm.get_match(game_id)

    if not match:
        bot.reply_to(m, 'Данная игра не запущена!')
        return
    if str(m.from_user.id) in match.session.player_ids:
        bot.reply_to(m, 'Вы уже в игре!')
        return
    if not match.lobby:
        bot.reply_to(m, 'Игра уже идет!')
        return
    match.join_session(m.from_user.id, m.from_user.full_name)

    bot.send_message(m.from_user.id, 'Вы вступили в игру! Осторжно, бот в бета тесте!')
    bot.send_message(game_id, f'{m.from_user.full_name} вступил в игру!')


@bot.message_handler(commands=['vd_go'])
def vd_join_handler(m):
    match = mm.get_match(m.chat.id)
    if not match:
        bot.reply_to(m, 'Игра не запущена! Запустите командой /vd_prepare.')
        return
    if str(m.from_user.id) not in match.session.player_ids:
        if m.from_user.id != admin:
            bot.reply_to(m, 'Вас нет в игре, не вам и запускать!')
            return
    if not match.lobby:
        bot.reply_to(m, 'Игра уже идет!')
        return
    match.lobby = False
    match.choose_items()
    match.choose_weapons()
    bot.reply_to(m, 'Игра начинается!')


@bot.callback_query_handler(func=lambda c: c.data == 'vd_go')
def act_callback_handler(c):
    match = mm.get_match(c.message.chat.id)
    if not match:
        bot.answer_callback_query(c.id, "Игра не запущена!")
        return
    if str(c.from_user.id) not in match.session.player_ids:
        if c.from_user.id != admin:
            bot.answer_callback_query(c.id, "Вас нет в игре!")
            return
    if not match.lobby:
        bot.answer_callback_query(c.id, "Игра уже идет!")
        return
    match.lobby = False
    match.choose_items()
    match.choose_weapons()
    bot.reply_to(c.message, 'Игра начинается!')


@bot.message_handler(commands=['vd_join'])
def vd_join_handler(m):
    match = mm.get_match(m.chat.id)
    if not match:
        bot.reply_to(m, 'Игра не запущена! Запустите командой /vd_prepare.')
        return
    if str(m.from_user.id) in match.session.player_ids:
        bot.reply_to(m, 'Вы уже в игре!')
        return
    if not match.lobby:
        bot.reply_to(m, 'Игра уже идет!')
        return
    try:
        bot.send_message(m.from_user.id, 'Вы вступили в игру! Осторжно, бот в бета тесте!')
    except:
        bot.reply_to(m, 'Сначала напишите мне в ЛС!')
        return
    bot.send_message(m.chat.id, f'{m.from_user.full_name} вступил в игру!')
    match.join_session(m.from_user.id, m.from_user.full_name)


@bot.message_handler(commands=['vd_suicide'])
def vd_join_handler(m):
    match = mm.get_match(m.chat.id)
    if not match:
        return
    player = match.session.get_player(m.from_user.id)
    if not player:
        return
    if match.lobby:
        return
    player.dead = True
    player.hp = 0
    if not match.session.unready_players:
        match.session.say(f'☠️|{player.name} совершает суицид.')
        match.cycle()


@bot.message_handler(commands=['add_cow'])
def vd_join_handler(m):
    match = mm.get_match(m.chat.id)
    if not m.text.count(' ') or not m.text.split(' ')[1].isdigit():
        bot.reply_to(m, 'Так нельзя. Напиши /add_cow число.')
        return
    count = int(m.text.split(' ')[1])
    if not (0 <= count <= 15):
        bot.reply_to(m, 'Неправильно. Введи число от 0 до 15')
        return
    if not match:
        bot.reply_to(m, 'Игра не запущена! Запустите командой /vd_prepare.')
        return
    if match.cowed:
        bot.reply_to(m, 'МУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ.')
        return
    match.cowed = True
    for _ in range(count):
        cow = Cow(match.session.id)
        match.session.entities.append(cow)
    mm.update_message(match)
    bot.send_message(m.chat.id, f'{count} коров прибежало!')


@bot.callback_query_handler(func=lambda c: c.data.startswith('cw'))
def act_callback_handler(c):
    _, game_id, weapon_id = c.data.split('_', 2)
    match = mm.get_match(game_id)
    if not match:
        bot.edit_message_text('Игра уже закончилась!', c.message.chat.id, c.message.message_id)
        return
    if match.lobby:
        bot.edit_message_text('Хватит спешить.', c.message.chat.id, c.message.message_id)
        return
    player = match.session.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Вы не в игре!', c.message.chat.id, c.message.message_id)
        return
    if player.chose_weapon:
        bot.edit_message_text(f'Хватит так поступать.', c.message.chat.id, c.message.message_id)
        return
    if weapon_id == 'random':
        weapon = random.choice(rebuild.all_weapons)(game_id, player.id)
    else:
        weapon = cm.get_weapon(weapon_id)(game_id, player.id)
    player.weapon = weapon
    player.chose_weapon = True
    if not match.session.not_chosen_weapon:
        bot.send_message(match.session.chat_id, f'Оружие выбрано.')
        match.choose_skills()

    bot.edit_message_text(f'Выбрано оружие: {weapon.name}', c.message.chat.id, c.message.message_id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('cs'))
def act_callback_handler(c):
    _, cycle, game_id, skill_id = c.data.split('_', 3)
    match = mm.get_match(int(game_id))
    if not match:
        bot.edit_message_text('Игра уже закончилась!', c.message.chat.id, c.message.message_id)
        return
    if match.lobby:
        bot.edit_message_text('Хватит спешить.', c.message.chat.id, c.message.message_id)
        return
    player = match.session.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Вы не в игре!', c.message.chat.id, c.message.message_id)
        return
    if player.chose_skills or player.skill_cycle == int(cycle):
        bot.edit_message_text(f'Хватит так поступать.', c.message.chat.id, c.message.message_id)
        return
    skill = cm.get_state(skill_id)
    if skill_id == 'random':
        variants = list(filter(lambda s: s.id not in [s.id for s in player.states], rebuild.all_skills))
        if not variants:
            variants = rebuild.all_skills
        skill = random.choice(variants)
    engine.attach_states(player, [skill])
    player.skill_cycle = int(cycle)

    if int(cycle) >= match.skill_cycles:
        player.chose_skills = True
    else:
        match.send_skill_choice_buttons(player, int(cycle) + 1)

    bot.edit_message_text(f'Выбран скилл: {skill.name}', c.message.chat.id, c.message.message_id)

    if not match.session.not_chosen_skills:
        tts = f'Способности выбраны, игра начинается! Выбор оружия:'
        for player in match.session.alive_entities:
            tts += f'\n{player.name}: {player.weapon.name}'
        bot.send_message(match.session.chat_id, tts)
        match.start_game()


@bot.callback_query_handler(func=lambda c: c.data.startswith('ci'))
def act_callback_handler(c):
    _, skill_id = c.data.split('_', 3)
    bot.answer_callback_query(c.id, cm.get_state(skill_id).description, show_alert=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith('wi'))
def act_callback_handler(c):
    _, weapon_id = c.data.split('_', 3)
    bot.answer_callback_query(c.id, cm.get_weapon(weapon_id).description, show_alert=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith('act_'))
def act_callback_handler(c):
    _, game_id, act_id = c.data.split('_', 2)
    match = mm.get_match(game_id)
    if not match:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = match.session.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    action = engine.action_manager.get_action(match.session, player, act_id)
    if not action:
        bot.edit_message_text('Кнопка стухла!', c.message.chat.id, c.message.message_id)
        return
    if action.blocked:
        bot.answer_callback_query(c.id, "Кнопка заблокирована!", show_alert=True)
        return

    target = player
    if not action.target_type.own == Own.SELF_ONLY:
        match.action_indexes.append(action)
        index = len(match.action_indexes) - 1
        match.choose_target(player, action.targets, index)
        bot.delete_message(c.message.chat.id, c.message.message_id)
        return

    bot.edit_message_text(f"Выбрано: {action.name} на {action.target.name}", c.message.chat.id, c.message.message_id)
    match.choose_act(c.from_user.id, target.id, act_id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('tgt_'))
def act_callback_handler(c):
    _, game_id, target_id, index = c.data.split('_', 3)
    match = mm.get_match(game_id)
    if not match:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = match.session.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    target = match.session.get_player(target_id)
    if not target:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    if len(match.action_indexes) < int(index) + 1:
        bot.edit_message_text('Все стухло!', c.message.chat.id, c.message.message_id)
        return
    action = match.action_indexes[int(index)]
    action.target = target
    bot.edit_message_text(f"Выбрано: {action.name} на {action.target.name}", c.message.chat.id, c.message.message_id)
    match.choose_act(c.from_user.id, target.id, action.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('back_'))
def act_callback_handler(c):
    _, game_id = c.data.split('_', 1)
    match = mm.get_match(game_id)
    if not match:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = match.session.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    kb = match.get_act_buttons(player)
    tts = match.get_act_text(player)
    bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith('more_'))
def act_callback_handler(c):
    _, game_id = c.data.split('_', 1)
    match = mm.get_match(game_id)
    if not match:
        bot.edit_message_text('Игра стухла!', c.message.chat.id, c.message.message_id)
        return
    player = match.session.get_player(c.from_user.id)
    if not player:
        bot.edit_message_text('Игрок стух!', c.message.chat.id, c.message.message_id)
        return
    kb = match.get_additional_buttons(player)
    bot.edit_message_text('Дополнительно:', c.message.chat.id, c.message.message_id, reply_markup=kb)


bot.infinity_polling()
