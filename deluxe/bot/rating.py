from deluxe.startup import bot
from config import admin
from deluxe.db.Rating import RatingManager

rm = RatingManager()


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
    C_a = round(1 / EWP_a, 2) - 1
    C_b = round(1 / EWP_b, 2) - 1
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
