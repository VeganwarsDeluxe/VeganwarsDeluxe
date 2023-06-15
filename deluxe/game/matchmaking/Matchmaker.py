import random
from telebot import types

from .TelegramSession import TelegramSession
from .TelegramEntity import TelegramEntity
import modern
from core.Skills.Skill import Skill


class Matchmaker:
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    def pre_move(self, chat_id):
        game = self.games.get(chat_id)
        game.pre_move(), game.stage('pre-move')
        if not game.active:
            if list(game.alive_entities):
                tts = f'Игра окончена! Победила команда {list(game.alive_entities)[0].name}!'
            else:
                tts = 'Игра окончена! Все погибли!'
            self.bot.send_message(game.chat_id, tts)
            del self.games[chat_id]

        for player in game.alive_entities:
            self.send_act_buttons(player, game)

    def get_act_buttons(self, player, game):
        first_row = []
        second_row = []
        all = []
        approach = []
        skip = []
        for action in player.actions:
            button = types.InlineKeyboardButton(text=action.name, callback_data=f"act_{game.chat_id}_{action.id}")
            if action.id in ['attack', 'reload']:
                first_row.append(button)
            elif action.id in ['dodge']:
                second_row.append(button)
            elif action.id in ['approach']:
                approach.append(button)
            elif action.id in ['skip', 'extinguish']:
                skip.append(button)
            else:
                all.append(button)

        kb = types.InlineKeyboardMarkup()
        first_row.reverse()
        kb.add(*first_row)
        kb.add(*second_row)
        for button in all:
            kb.add(button)
        kb.add(*approach)
        kb.add(*skip)
        return kb

    def choose_target(self, game, player, targets):
        kb = types.InlineKeyboardMarkup()
        for target in targets:
            kb.add(types.InlineKeyboardButton(
                text=target.name, callback_data=f"tgt_{game.chat_id}_{target.id}"
            ))
        kb.add(types.InlineKeyboardButton(
                text='Назад', callback_data=f"back_{game.chat_id}"
            ))
        self.bot.send_message(player.id, 'Вьібор цели!', reply_markup=kb)

    def choose_act(self, game: TelegramSession, user_id, act_id):
        player = game.get_player(user_id)
        action = player.get_action(act_id)
        player.action = action

        targets = player.action.targets
        if not action.target_type.own == 1:
            self.choose_target(game, player, targets)
            return
        player.target = player
        player.ready = True
        player.action.target = player
        if not game.unready_players:
            self.cycle(game)

    def cycle(self, game):
        game.say(f'Ход {game.turn}:')
        game.move()
        for text in game.texts:
            if not text:
                continue
            for tts in text.split('\n\n'):
                self.bot.send_message(game.chat_id, tts)
        self.pre_move(game.chat_id)

    def send_act_buttons(self, player, game):
        kb = self.get_act_buttons(player, game)
        tts = f"Ход {game.turn}\n" \
              f"{'♥️' * player.hp}|{player.hp} жизней. Максимум: {player.max_hp}\n" \
              f"{'⚡️' * player.energy}|{player.energy}. Максимум: {player.max_energy}\n" \
              f"🎯|Вероятность попасть - {int(player.hit_chance)}%"
        self.bot.send_message(player.id, tts, reply_markup=kb)

    def get_skill(self, skill_id, player):
        skills = list(filter(lambda s: s(player).id == skill_id, modern.all_skills))
        return skills[0](player) if skills else Skill(player)

    def get_weapon(self, weapon_id, player):
        weapons = list(filter(lambda w: w(player).id == weapon_id, modern.all_weapons))
        return weapons[0](player) if weapons else modern.Fist(player)

    def get_game(self, chat_id):
        return self.games.get(chat_id)

    def create_game(self, chat_id):
        self.games.update({chat_id: TelegramSession(chat_id)})
        return self.get_game(chat_id)

    def join_game(self, chat_id, user_id, user_name):
        game = self.games.get(chat_id)

        player = TelegramEntity(game, user_name, user_id)
        player.energy, player.max_energy, player.hp, player.max_hp = 5, 5, 4, 4
        game.entities.append(player)

    def choose_weapons(self, chat_id):
        game = self.games.get(chat_id)
        for player in game.not_chosen_weapon:
            self.send_weapon_choice_buttons(player)

    def choose_skills(self, chat_id):
        game = self.games.get(chat_id)
        for player in game.not_chosen_skills:
            self.send_skill_choice_buttons(player)

    def send_weapon_choice_buttons(self, player, number=3):
        weapons, clss = [modern.Flamethrower(player)], [modern.Flamethrower]
        for _ in range(number):
            variants = list(filter(lambda w: w not in clss, modern.all_weapons))
            if not variants:
                break
            choice = random.choice(variants)
            weapons.append(choice(player))
            clss.append(choice)

        kb = types.InlineKeyboardMarkup()
        for weapon in weapons:
            kb.add(types.InlineKeyboardButton(text=weapon.name,
                                              callback_data=f"cw_{player.session.chat_id}_{weapon.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайное оружие',
                                          callback_data=f"cw_{player.session.chat_id}_random"))
        self.bot.send_message(player.id, 'Выберите оружие:', reply_markup=kb)

    def send_skill_choice_buttons(self, player, number=5, cycle=1):
        game = player.session
        skills, clss = [], []
        for _ in range(number):
            variants = list(filter(lambda s: s not in clss, modern.all_skills))
            if not variants:
                break
            choice = random.choice(variants)
            skills.append(choice(player))
            clss.append(choice)

        kb = types.InlineKeyboardMarkup()
        for skill in skills:
            kb.add(types.InlineKeyboardButton(text=skill.name,
                                              callback_data=f"cs_{cycle}_{player.session.chat_id}_{skill.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайный скилл',
                                          callback_data=f"cs_{cycle}_{player.session.chat_id}_random"))
        self.bot.send_message(player.id, f'Выберите скилл ({cycle} из {game.skill_cycles}):', reply_markup=kb)
