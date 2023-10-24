from mongoengine import connect, DoesNotExist
from telebot import TeleBot, types
from config import rpg_token, mongourl

from rpg.db.User import User
from rpg.db.Item import Item, generate_object_code, create_item, create_unscroll, create_recipe

from rpg.texts import *

bot = TeleBot(rpg_token)
connect(host=mongourl, db='vegan_rpg')


def main_menu_keyboard(m):
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton(ATTACK_COMMAND),
           types.KeyboardButton(DEFEND_COMMAND),
           types.KeyboardButton(QUESTS_COMMAND))
    kb.add(types.KeyboardButton(PROFILE_COMMAND),
           types.KeyboardButton(INVENTORY_COMMAND),
           types.KeyboardButton(CASTLE_COMMAND))
    kb.add(types.KeyboardButton(ABILITIES_COMMAND), types.KeyboardButton(ITEMS_COMMAND))
    return kb


def no_castle_menu_keyboard(m):
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton(RAT_CASTLE+JOIN_MARK), types.KeyboardButton(DARK_CASTLE+JOIN_MARK))
    kb.add(types.KeyboardButton(NECROMANCER_CASTLE+JOIN_MARK), types.KeyboardButton(EXPLOSION_CASTLE+JOIN_MARK))
    kb.add(types.KeyboardButton(NO_CASTLE_REST_COMMAND))
    kb.add(types.KeyboardButton(PROFILE_COMMAND))
    return kb


def shop_menu_keyboard(m):
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton(SCROLLS_SHOP_COMMAND), types.KeyboardButton(EQUIPMENT_SHOP_COMMAND))
    kb.add(types.KeyboardButton(DEC_SCROLL_COMMAND), types.KeyboardButton(DEC_RECIPE_COMMAND))
    kb.add(types.KeyboardButton(PROFILE_COMMAND))
    return kb


def castle_menu_keyboard(m):
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton(SHOP_COMMAND), types.KeyboardButton(CRAFT_COMMAND))
    kb.add(types.KeyboardButton(AUCTION_COMMAND), types.KeyboardButton(TRADE_COMMAND))
    kb.add(types.KeyboardButton(REST_COMMAND))
    kb.add(types.KeyboardButton(PROFILE_COMMAND))
    return kb


def attack_menu_keyboard(m):
    user = User.objects.get(id=m.from_user.id)

    kb = types.ReplyKeyboardMarkup()
    for button, castle in CASTLE_ATTACK_BUTTONS.items():
        if user.castle == castle:
            continue
        kb.add(types.KeyboardButton(button))

    kb.add(types.KeyboardButton(PROFILE_COMMAND))
    return kb


@bot.message_handler(commands=['start'])
def start_handler(m):
    bot.reply_to(m, 'Идет разработка. Пожалуйста подождите.',
                 reply_markup=main_menu_keyboard(m) if m.chat.type == 'private' else None)


@bot.message_handler(func=lambda m: m.chat.type != 'private')
def non_private_handler(m):
    pass


@bot.message_handler(func=lambda m: False)
def private_handler(m):
    try:
        user = User.objects.get(id=m.from_user.id)
    except DoesNotExist:
        user = User(id=m.from_user.id)
        user.username = m.from_user.username or None
        user.save()
    return user


@bot.message_handler(func=lambda m: private_handler(m) and False)
def lambda_private_handler(m):
    pass


@bot.message_handler(func=lambda m: m.text == PROFILE_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    bot.reply_to(m, user.get_profile_text(), reply_markup=main_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == CASTLE_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    if user.castle == 'outsider':
        bot.reply_to(m, NO_CASTLE_PLEASE_JOIN, reply_markup=no_castle_menu_keyboard(m))
        return
    bot.reply_to(m, CASTLE_ENTRANCE_TEXT, reply_markup=castle_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == SHOP_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    if user.castle == 'outsider':
        bot.reply_to(m, NO_CASTLE_PLEASE_JOIN, reply_markup=no_castle_menu_keyboard(m))
        return

    tts = "📜Свитки - Древние записи о ведении боя и его техниках. С помощью них можно изучить новые скиллы.\n\n" \
          "⚙️Снаряжение - оружейная мастерская старого кузнеца. Простое, но надёжное оружие."
    bot.reply_to(m, tts, reply_markup=shop_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == DEC_RECIPE_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    if user.castle == 'outsider':
        bot.reply_to(m, NO_CASTLE_PLEASE_JOIN, reply_markup=no_castle_menu_keyboard(m))
        return

    tts = "Вы находитесь в отделе лавки, который занимается расшифровкой древних записей. " \
          "За хорошую цену, разумеется. Чтобы расшифровать рецепт, нажмите соответствующую команду.\n\n"
    for item in user.items:
        if item.type == 'recipe':
            tts += f'{item.emoji}|{item.name}: 💰100 /dec_{item.object_code}\n'
    bot.reply_to(m, tts, reply_markup=shop_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == DEC_SCROLL_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    if user.castle == 'outsider':
        bot.reply_to(m, NO_CASTLE_PLEASE_JOIN, reply_markup=no_castle_menu_keyboard(m))
        return

    tts = "Вы находитесь в отделе лавки, который занимается расшифровкой древних записей. " \
          "За хорошую цену, разумеется. Чтобы расшифровать свиток, нажмите соответствующую команду.\n\n"
    for item in user.items:
        if item.type == 'unscroll':
            tts += f'{item.emoji}|{item.name}: 💰100 /dec_{item.object_code}\n'
    bot.reply_to(m, tts, reply_markup=shop_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == ATTACK_COMMAND)
def start_handler(m):
    bot.reply_to(m, "Выберите замок для атаки:", reply_markup=attack_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == DEFEND_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    if user.castle == 'outsider':
        bot.reply_to(m, NO_CASTLE_PLEASE_JOIN, reply_markup=no_castle_menu_keyboard(m))
        return
    user.current_action = 'defense'
    user.save()
    bot.reply_to(m, "Вы приготовились к защите замка. Битва через хз сколько, как Брит начнет.",
                 reply_markup=main_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text in CASTLE_ATTACK_BUTTONS)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    attack_target = CASTLE_ATTACK_BUTTONS[m.text]
    if attack_target == user.castle:
        bot.reply_to(m, 'Свой замок атаковать нельзя!', reply_markup=main_menu_keyboard(m))
        return
    user.current_action = 'attack'
    user.attack_target = attack_target
    user.save()
    bot.reply_to(m, f"Вы приготовились к атаке на {CASTLE_ID_TO_TEXT.get(attack_target)}. "
                    f"Битва через хз сколько, как Брит начнет.",
                 reply_markup=main_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == REST_COMMAND or m.text == NO_CASTLE_REST_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    user.current_action = 'rest'
    user.save()
    bot.reply_to(m, "Вы прилегли отдохнуть. Все действия отменились.",
                 reply_markup=main_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text == INVENTORY_COMMAND)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    if not user.items:
        item = Item(object_code=generate_object_code(), name="Тортик", emoji="🎂", description="Тортик для новеньких!")
        user.items.append(item)
        bot.send_message(m.chat.id, "Вам дали тортик, потому что у вас не нашлось ничего в инвентаре!")
    tts = "📦Ваш инвентарь:\n\n"
    for item in user.items:
        item: Item
        tts += f"{item.emoji}|{item.name} /info_{item.object_code}\n"
    user.save()
    bot.reply_to(m, tts, reply_markup=main_menu_keyboard(m))


@bot.message_handler(func=lambda m: m.text in CASTLE_JOIN_BUTTONS)
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    if user.castle != 'outsider':
        bot.reply_to(m, "Вы уже состоите в замке.", reply_markup=main_menu_keyboard(m))
        return
    castle = CASTLE_JOIN_BUTTONS[m.text]
    bot.reply_to(m, f"Добро пожаловать в замок {castle}! Ссылка на ваш замковый чат: [CASTLE_LINK].",
                 reply_markup=main_menu_keyboard(m))
    user.castle = castle
    user.save()


@bot.message_handler(func=lambda m: m.text.startswith('/info_'))
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    item_code = m.text.split('_', 1)[1]
    item = user.get_item(item_code)
    if not item:
        bot.reply_to(m, 'Такого предмета у вас нет!')
    bot.reply_to(m, f'{item.emoji}|{item.description}')


@bot.message_handler(commands=['debug'])
def start_handler(m):
    user = User.objects.get(id=m.from_user.id)
    user.items.append(create_unscroll())
    user.items.append(create_recipe('red'))
    user.items.append(create_recipe('blue'))
    user.items.append(create_recipe('green'))
    user.items.append(create_recipe('huh'))
    user.save()

    bot.reply_to(m, 'Держите набор для дебага.')


bot.polling()
