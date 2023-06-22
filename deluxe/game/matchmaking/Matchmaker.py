import random
from telebot import types

from .TelegramSession import TelegramSession
from deluxe.game.Entities.TelegramEntity import TelegramEntity
import modern
from core.Skills.Skill import Skill


class Matchmaker:
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    def pre_move(self, chat_id):
        game = self.games.get(chat_id)
        game.update_actions()
        game.pre_move(), game.stage('pre-move')
        if not game.active:
            if list(game.alive_entities):
                tts = f'Игра окончена! Победила команда {list(game.alive_entities)[0].name}!'
            else:
                tts = 'Игра окончена! Все погибли!'
            self.bot.send_message(game.chat_id, tts)
            for player in game.entities:
                if player.id == game.chat_id:
                    continue
                try:
                    if player.id == game.chat_id:
                        continue
                    self.bot.send_message(player.id, tts)
                except:
                    pass
            del self.games[chat_id]
            return

        for player in game.alive_entities:
            if player.npc:
                player.choose_act()
            else:
                self.send_act_buttons(player, game)

        if not game.unready_players:
            self.cycle(game)

    def get_act_buttons(self, player, game):
        first_row = []
        second_row = []
        all = []
        items = []
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

        for item in player.items:
            items.append(types.InlineKeyboardButton(text=item.name, callback_data=f"item_{game.chat_id}_{item.id}"))

        kb = types.InlineKeyboardMarkup()
        first_row.reverse()
        second_row.append(
            types.InlineKeyboardButton(text='Инфо', callback_data='ci_777')
        )

        kb.add(*first_row)
        kb.add(*second_row)
        kb.add(types.InlineKeyboardButton(
            text='Дополнительно', callback_data=f"more_{game.chat_id}"
        ))
        kb.add(*approach)
        kb.add(*skip)
        return kb

    def get_additional_buttons(self, player, game):
        all = []
        items = []
        for action in player.actions:
            button = types.InlineKeyboardButton(text=action.name, callback_data=f"act_{game.chat_id}_{action.id}")
            if action.id in ['attack', 'reload', 'approach', 'dodge', 'skip', 'extinguish']:
                pass
            else:
                all.append(button)

        item_count = {}
        for item in player.items:
            if (item.id, item.name) not in item_count:
                item_count[(item.id, item.name)] = 1
            else:
                item_count[(item.id, item.name)] += 1
        for item_id, item_name in item_count:
            items.append(types.InlineKeyboardButton(
                text=f"{item_name} ({item_count[(item_id, item_name)]})", callback_data=f"item_{game.chat_id}_{item_id}"
            ))

        kb = types.InlineKeyboardMarkup()
        for button in all:
            kb.add(button)
        for button in items:
            kb.add(button)
        kb.add(types.InlineKeyboardButton(
            text='Назад', callback_data=f"back_{game.chat_id}"
        ))
        return kb

    def choose_item_target(self, game, player, targets, index=-1):
        kb = types.InlineKeyboardMarkup()
        for target in targets:
            kb.add(types.InlineKeyboardButton(
                text=target.name, callback_data=f"itgt_{game.chat_id}_{target.id}_{index}"
            ))
        kb.add(types.InlineKeyboardButton(
            text='Назад', callback_data=f"back_{game.chat_id}"
        ))
        self.bot.send_message(player.id, 'Вьібор цели!', reply_markup=kb)

    def choose_target(self, game, player, targets, index=-1):
        kb = types.InlineKeyboardMarkup()
        for target in targets:
            kb.add(types.InlineKeyboardButton(
                text=target.name, callback_data=f"tgt_{game.chat_id}_{target.id}_{index}"
            ))
        kb.add(types.InlineKeyboardButton(
            text='Назад', callback_data=f"back_{game.chat_id}"
        ))
        self.bot.send_message(player.id, 'Вьібор цели!', reply_markup=kb)

    def choose_item(self, game: TelegramSession, user_id, act_id):
        player = game.get_player(user_id)
        item = player.get_item(act_id)
        index = -1
        if item.cost < 1:
            item.canceled = False
            player.item_queue.append(item)
            player.items.remove(item)
            index = len(player.item_queue) - 1
        else:
            player.action = item

        targets = item.targets
        if not item.target_type.own == 1:
            self.choose_item_target(game, player, targets, index)
            return
        item.target = player
        player.target = player
        if item.cost < 1:
            self.send_act_buttons(player, game)
            return
        player.ready = True
        if not game.unready_players:
            self.cycle(game)

    def choose_act(self, game: TelegramSession, user_id, act_id):
        player = game.get_player(user_id)
        action = player.get_action(act_id)
        index = -1
        if action.cost < 1:
            player.action_queue.append(action)
            index = len(player.action_queue) - 1
        else:
            player.action = action
        action.canceled = False

        targets = action.targets
        if not action.target_type.own == 1:
            self.choose_target(game, player, targets, index)
            return
        action.target = player
        player.target = player
        if action.cost < 1:
            if action.cost == -1:
                action()
                player.action_queue.remove(action)
                player.update_actions()
            self.send_act_buttons(player, game)
            return
        player.ready = True
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
                for player in game.entities:
                    try:
                        if player.id == game.chat_id:
                            continue
                        self.bot.send_message(player.id, tts)
                    except:
                        pass
        self.pre_move(game.chat_id)

    def send_act_buttons(self, player, game):
        kb = self.get_act_buttons(player, game)
        tts = self.get_act_text(player, game)
        self.bot.send_message(player.id, tts, reply_markup=kb)

    def get_act_text(self, player, game):
        tts = f"Ход {game.turn}\n" \
              f"{player.hearts}|{player.hp} жизней. Максимум: {player.max_hp}\n" \
              f"{player.energies}|{player.energy} энергии. Максимум: {player.max_energy}\n" \
              f"🎯|Вероятность попасть - {int(player.hit_chance)}%\n"
        if player.weapon.id == 11 and player.weapon.main_target[0]:
            target, power = player.weapon.main_target
            chance = player.hit_chance
            if power == 1:
                chance += 60
            elif power == 1:
                chance += 90
            tts += f'🎯|Вероятность попасть в {target.name}|🎃 - {chance}%'
        return tts

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

    def choose_items(self, chat_id):
        game = self.games.get(chat_id)
        for player in game.not_chosen_items:
            given = []
            for _ in range(game.items_given):
                item = random.choice(modern.game_items_pool)(player)
                pool = list(filter(lambda i: i(player).id not in given, modern.game_items_pool))
                if pool:
                    item = random.choice(pool)(player)
                given.append(item.id)
                player.items.append(item)
            player.chose_items = True
            if player.npc:
                continue
            self.bot.send_message(player.id, f'Ваши предметы: '
                                             f'{", ".join([item.name for item in player.items])}')

    def choose_weapons(self, chat_id):
        game = self.games.get(chat_id)
        for player in game.not_chosen_weapon:
            if player.npc:
                continue
            self.send_weapon_choice_buttons(player)
        if not game.not_chosen_weapon:
            self.bot.send_message(game.chat_id, f'Оружие выбрано.')
            self.choose_skills(int(chat_id))

    def choose_skills(self, chat_id):
        game = self.games.get(chat_id)
        for player in game.not_chosen_skills:
            if player.npc:
                continue
            self.send_skill_choice_buttons(player)
        if not game.not_chosen_skills:
            tts = f'Способности выбраны, игра начинается! Выбор оружия:'
            for player in game.alive_entities:
                tts += f'\n{player.name}: {player.weapon.name}'
            self.bot.send_message(game.chat_id, tts)
            self.pre_move(game.chat_id)

    def send_weapon_choice_buttons(self, player, number=3):
        weapons = [modern.Saber]
        for _ in range(number):
            variants = list(filter(lambda w: w.id not in [w.id for w in weapons], modern.all_weapons))
            if not variants:
                break
            choice = random.choice(variants)
            weapons.append(choice(player))

        kb = types.InlineKeyboardMarkup()
        for weapon in weapons:
            kb.add(types.InlineKeyboardButton(weapon.name, callback_data=f"cw_{player.session.chat_id}_{weapon.id}"),
                   types.InlineKeyboardButton('Информация', callback_data=f"wi_{weapon.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайное оружие',
                                          callback_data=f"cw_{player.session.chat_id}_random"))
        self.bot.send_message(player.id, 'Выберите оружие:', reply_markup=kb)

    def send_skill_choice_buttons(self, player, number=5, cycle=1):
        game = player.session
        skills = []
        for _ in range(number):
            variants = list(filter(lambda s: s.id not in [s.id for s in skills], modern.all_skills))
            if not variants:
                break
            choice = random.choice(variants)
            skills.append(choice(player))

        kb = types.InlineKeyboardMarkup()
        for skill in skills:
            kb.add(
                types.InlineKeyboardButton(skill.name, callback_data=f"cs_{cycle}_{player.session.chat_id}_{skill.id}"),
                types.InlineKeyboardButton('Информация', callback_data=f"ci_{skill.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайный скилл',
                                          callback_data=f"cs_{cycle}_{player.session.chat_id}_random"))
        self.bot.send_message(player.id, f'Выберите скилл ({cycle} из {game.skill_cycles}):', reply_markup=kb)
