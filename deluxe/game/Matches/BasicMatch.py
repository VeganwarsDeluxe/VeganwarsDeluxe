import random

import telebot.util
from telebot import types

from VegansDeluxe import rebuild

from VegansDeluxe.core import PreMoveGameEvent

from deluxe.game.Entities.TelegramEntity import TelegramEntity
from deluxe.game.Sessions.TelegramSession import TelegramSession
from deluxe.startup import bot, engine


class BasicMatch:
    name = "Basic"

    def __init__(self, chat_id):
        self.bot = bot

        self.id = str(chat_id)
        self.session = self.create_session(self.id)

        self.lobby_message = None
        self.lobby = True

        self.skill_cycles = 2
        self.skill_number = 5

        self.weapon_number = 3

        self.items_given = 2

        self.cowed = False

        self.action_indexes = []

    def join_session(self, user_id, user_name) -> TelegramEntity:
        player = TelegramEntity(self.session.id, user_name, user_id)
        player.energy, player.max_energy, player.hp, player.max_hp = 5, 5, 4, 4
        self.session.entities.append(player)
        return player

    def create_session(self, id: str):
        session = TelegramSession(id)
        engine.session_manager.attach_session(session)
        return session

    def notify_players(self, message):
        """Notifies all players in the game."""
        for player in self.session.entities:
            try:
                # Skip if the player is an NPC or if the user is the one who initiated the game
                if player.user_id == self.session.chat_id or player.npc:
                    continue
                bot.send_message(player.user_id, message)
            except Exception as e:
                print(f"Failed to send message to player {player.user_id}. Error: {str(e)}")

    def send_end_game_messages(self):
        """Sends messages when the game ends."""
        if list(self.session.alive_entities):
            tts = f'Игра окончена! Победила команда {list(self.session.alive_entities)[0].name}!'
        else:
            tts = 'Игра окончена! Все погибли!'
        self.notify_players(tts)
        bot.send_message(self.session.chat_id, tts)
        engine.session_manager.delete_session(self.session.id)

    def choose_target(self, player, targets, index=0):
        kb = types.InlineKeyboardMarkup()
        for target in targets:
            kb.add(types.InlineKeyboardButton(
                text=target.name, callback_data=f"tgt_{self.session.chat_id}_{target.id}_{index}"
            ))
        kb.add(types.InlineKeyboardButton(
            text='Назад', callback_data=f"back_{self.session.chat_id}"
        ))
        bot.send_message(player.user_id, 'Выбор цели:', reply_markup=kb)

    def choose_act(self, user_id, target_id, act_id):
        player = self.session.get_player(user_id)
        target = self.session.get_entity(target_id)
        action = engine.action_manager.get_action(self.session, player, act_id)
        queue = engine.action_manager.queue_action(self.session, player, act_id)
        action.target = target

        if action.type == 'item':
            player.items.remove(action.item)

        if queue:
            self.send_act_buttons(player)
            return
        player.ready = True
        if not self.session.unready_players:
            self.cycle()

    def process_game_texts(self):
        for text in self.session.texts:
            if not text:
                continue
            for message in text.split('\n\n'):
                new_message = self.merge_lines(message)

                for tts in telebot.util.smart_split(new_message):
                    bot.send_message(self.session.chat_id, tts)
                    self.notify_players(tts)

    def merge_lines(self, text):
        new_message = ''

        previous_line = ''
        counter = 0
        for line in text.split('\n'):
            if line == previous_line:
                counter += 1
                continue
            elif counter > 1:
                new_message += f'Сообщение сверху повторилось {counter} раз.\n'
            previous_line = line
            counter = 0
            new_message += line + '\n'
        return new_message

    def send_act_buttons(self, player):
        kb = self.get_act_buttons(player)
        tts = self.get_act_text(player)
        bot.send_message(player.user_id, tts, reply_markup=kb)

    def get_act_text(self, player):
        tts = f"Ход {self.session.turn}\n" \
              f"{player.hearts}|{player.hp} жизней. Максимум: {player.max_hp}\n" \
              f"{player.energies}|{player.energy} энергии. Максимум: {player.max_energy}\n"
        tts += f"🎯|Вероятность попасть - {int(player.weapon.hit_chance(player))}%\n" if player.weapon else ''

        tts += player.notifications

        return tts

    def start_game(self):
        """Starts a game."""
        self.session.start()
        self.pre_move()

    def update_game_actions(self):
        """Updates actions for a game."""
        engine.action_manager.update_actions(self.session)
        self.action_indexes = []

    def handle_pre_move_events(self):
        """Handles events before a move."""
        self.session.pre_move(), engine.event_manager.publish(PreMoveGameEvent(self.session.id, self.session.turn))

    def execute_actions(self):
        """Executes actions for all alive entities."""
        for player in self.session.alive_entities:
            if player.get_state('stun').stun:
                engine.action_manager.queue_action(self.session, player, 'lay_stun')
                player.ready = True
                if not self.session.unready_players:
                    self.cycle()
            elif player.npc:
                player.choose_act(self.session)
            else:
                self.send_act_buttons(player)

    def map_buttons(self, player):
        engine.action_manager.update_entity_actions(self.session, player)

        buttons = {
            'first_row': [],
            'second_row': [],
            'additional': [],
            'approach_row': [],
            'skip_row': []
        }
        for action in engine.action_manager.get_available_actions(self.session, player):
            name = action.name
            button = types.InlineKeyboardButton(text=name, callback_data=f"act_{self.session.chat_id}_{action.id}")
            if action.id in ['attack', 'reload']:
                buttons['first_row'].append(button)
            elif action.id in ['dodge']:
                buttons['second_row'].append(button)
            elif action.id in ['approach']:
                buttons['approach_row'].append(button)
            elif action.id in ['skip', 'extinguish']:
                buttons['skip_row'].append(button)
            else:
                buttons['additional'].append(button)
        return buttons

    def get_act_buttons(self, player):
        buttons = self.map_buttons(player)

        kb = types.InlineKeyboardMarkup()
        buttons['first_row'].reverse()
        buttons['second_row'].append(
            types.InlineKeyboardButton(text='Инфо', callback_data='ci_777')
        )

        kb.add(*buttons['first_row'])
        kb.add(*buttons['second_row'])
        kb.add(types.InlineKeyboardButton(
            text='Дополнительно', callback_data=f"more_{self.session.chat_id}"
        ))
        kb.add(*buttons['approach_row'])
        kb.add(*buttons['skip_row'])
        return kb

    def get_additional_buttons(self, player):
        engine.action_manager.update_entity_actions(self.session, player)

        all_buttons = []
        items = []
        for action in engine.action_manager.get_available_actions(self.session, player):
            name = action.name
            if action.type == 'item':
                items.append(action)
                continue
            button = types.InlineKeyboardButton(text=name, callback_data=f"act_{self.session.chat_id}_{action.id}")
            if action.id in ['attack', 'reload', 'approach', 'dodge', 'skip', 'extinguish']:
                pass
            else:
                all_buttons.append(button)

        item_count = {}
        for item_action in items:
            if item_action.item.id not in item_count:
                item_count[item_action.item.id] = 0
            item_count[item_action.item.id] += 1

        item_buttons = []
        added_items = []
        for action in items:
            if action.item.id in added_items:
                continue
            name = f"{action.name} ({item_count[action.item.id]})"
            button = types.InlineKeyboardButton(text=name, callback_data=f"act_{self.session.chat_id}_{action.id}")
            item_buttons.append(button)
            added_items.append(action.item.id)

        kb = types.InlineKeyboardMarkup()
        for button in all_buttons:
            kb.add(button)
        for button in item_buttons:
            kb.add(button)
        kb.add(types.InlineKeyboardButton(
            text='Назад', callback_data=f"back_{self.session.chat_id}"
        ))
        return kb

    def check_game_status(self):
        """Checks the status of the game and sends end game messages if needed."""
        if not self.session.active:
            self.send_end_game_messages()
            return False
        return True

    def pre_move(self):
        """Handles pre-move procedures."""
        self.update_game_actions()
        self.handle_pre_move_events()
        if not self.check_game_status():
            return
        self.execute_actions()
        if not self.session.unready_players:
            self.cycle()

    def cycle(self):
        if not self.check_game_status():
            return
        self.session.say(f'Ход {self.session.turn}:')
        self.session.move()
        self.process_game_texts()
        self.pre_move()

    def choose_items(self):
        for player in self.session.not_chosen_items:
            given = []
            for _ in range(self.items_given):
                item = random.choice(rebuild.game_items_pool)()
                pool = list(filter(lambda i: i.id not in given, rebuild.game_items_pool))
                if pool:
                    item = random.choice(pool)()
                given.append(item.id)
                player.items.append(item)
            player.chose_items = True
            if player.npc:
                continue
            bot.send_message(player.user_id, f'Ваши предметы: '
                                             f'{", ".join([item.name for item in player.items])}')

    def choose_weapons(self):
        for player in self.session.not_chosen_weapon:
            if player.npc:
                continue
            self.send_weapon_choice_buttons(player)
        if not self.session.not_chosen_weapon:
            bot.send_message(self.session.chat_id, f'Оружие выбрано.')
            self.choose_skills()

    def choose_skills(self):
        for player in self.session.not_chosen_skills:
            if player.npc:
                continue
            self.send_skill_choice_buttons(player)
        if not self.session.not_chosen_skills:
            weapons_text = '\n'.join([f'{player.name}: {player.weapon.name}' for player in self.session.alive_entities])
            bot.send_message(self.session.chat_id, f'Способности выбраны, игра начинается! '
                                                   f'Выбор оружия:\n{weapons_text}')
            self.pre_move()

    def send_weapon_choice_buttons(self, player):
        weapons = []
        for _ in range(self.weapon_number):
            variants = list(filter(lambda w: w.id not in [w.id for w in weapons], rebuild.all_weapons))
            if not variants:
                break
            choice = random.choice(variants)
            weapons.append(choice)

        weapons.sort(key=lambda w: w.id)

        kb = types.InlineKeyboardMarkup()
        for weapon in weapons:
            kb.add(types.InlineKeyboardButton(weapon.name, callback_data=f"cw_{self.session.chat_id}_{weapon.id}"),
                   types.InlineKeyboardButton('Информация', callback_data=f"wi_{weapon.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайное оружие',
                                          callback_data=f"cw_{self.session.chat_id}_random"))
        bot.send_message(player.user_id, 'Выберите оружие:', reply_markup=kb)

    def send_skill_choice_buttons(self, player, cycle=1):
        skills = []
        for _ in range(self.skill_number):
            variants = list(filter(lambda s: s.id not in [s.id for s in skills], rebuild.all_skills))
            variants = list(filter(lambda s: s.id not in [s.id for s in player.states], variants))
            if not variants:
                break
            choice = random.choice(variants)
            skills.append(choice)

        skills.sort(key=lambda s: s.id)

        kb = types.InlineKeyboardMarkup()
        for skill in skills:
            kb.add(
                types.InlineKeyboardButton(skill.name, callback_data=f"cs_{cycle}_{self.session.chat_id}_{skill.id}"),
                types.InlineKeyboardButton('Информация', callback_data=f"ci_{skill.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайный скилл',
                                          callback_data=f"cs_{cycle}_{self.session.chat_id}_random"))
        bot.send_message(player.user_id, f'Выберите скилл ({cycle} из {self.skill_cycles}):', reply_markup=kb)
