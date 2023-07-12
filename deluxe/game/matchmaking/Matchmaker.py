import random
from telebot import types
from core.Actions.ActionManager import action_manager
from core.Events.EventManager import event_manager
from core.Events.Events import PreMoveGameEvent
from core.SessionManager import SessionManager
from .TelegramSession import TelegramSession
from deluxe.game.Entities.TelegramEntity import TelegramEntity
import modern
from core.Skills.Skill import Skill

# TODO: Refactor


class Matchmaker:
    """Matchmaker Class: Handles game setup, turns, and messages."""

    def __init__(self, bot):
        """Initialization function."""
        self.bot = bot
        self.session_manager = SessionManager()
        self.action_indexes = []

    def start_game(self, game):
        """Starts a game."""
        game.start()
        self.pre_move(game.chat_id)

    def pre_move(self, chat_id):
        """Handles pre-move procedures."""
        game = self.get_game(chat_id)
        self.update_game_actions(game)
        self.handle_pre_move_events(game)
        self.check_game_status(game)
        self.execute_actions(game)
        if not game.unready_players:
            self.cycle(game)

    def update_game_actions(self, game):
        """Updates actions for a game."""
        action_manager.update_actions(game)
        self.action_indexes = []

    def handle_pre_move_events(self, game):
        """Handles events before a move."""
        game.pre_move(), event_manager.publish(PreMoveGameEvent(game.id, game.turn))

    def check_game_status(self, game):
        """Checks the status of the game and sends end game messages if needed."""
        if not game.active:
            self.send_end_game_messages(game)

    def notify_players(self, game, message):
        """Notifies all players in the game."""
        for player in game.entities:
            try:
                # Skip if the player is an NPC or if the user is the one who initiated the game
                if player.user_id == game.chat_id or player.npc:
                    continue
                self.bot.send_message(player.user_id, message)
            except Exception as e:
                print(f"Failed to send message to player {player.user_id}. Error: {str(e)}")

    def send_end_game_messages(self, game):
        """Sends messages when the game ends."""
        if list(game.alive_entities):
            tts = f'Игра окончена! Победила команда {list(game.alive_entities)[0].name}!'
        else:
            tts = 'Игра окончена! Все погибли!'
        self.notify_players(game, tts)
        self.bot.send_message(game.chat_id, tts)
        self.session_manager.delete_session(game.id)

    def execute_actions(self, game):
        """Executes actions for all alive entities."""
        for player in game.alive_entities:
            if player.get_skill('stun').stun:
                action_manager.queue_action(game, player, 'lay_stun')
                player.ready = True
                if not game.unready_players:
                    self.cycle(game)
            elif player.npc:
                player.choose_act(game)
            else:
                self.send_act_buttons(player, game)

    def get_act_buttons(self, player, game):
        action_manager.update_entity_actions(game, player)

        first_row = []
        second_row = []
        all_buttons = []
        approach = []
        skip = []
        for action in action_manager.get_available_actions(game, player):
            name = action.name
            button = types.InlineKeyboardButton(text=name, callback_data=f"act_{game.chat_id}_{action.id}")
            if action.id in ['attack', 'reload']:
                first_row.append(button)
            elif action.id in ['dodge']:
                second_row.append(button)
            elif action.id in ['approach']:
                approach.append(button)
            elif action.id in ['skip', 'extinguish']:
                skip.append(button)
            else:
                all_buttons.append(button)

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
        action_manager.update_entity_actions(game, player)

        all_buttons = []
        items = []
        for action in action_manager.get_available_actions(game, player):
            name = action.name
            if action.type == 'item':
                items.append(action)
                continue
            button = types.InlineKeyboardButton(text=name, callback_data=f"act_{game.chat_id}_{action.id}")
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
            button = types.InlineKeyboardButton(text=name, callback_data=f"act_{game.chat_id}_{action.id}")
            item_buttons.append(button)
            added_items.append(action.item.id)

        kb = types.InlineKeyboardMarkup()
        for button in all_buttons:
            kb.add(button)
        for button in item_buttons:
            kb.add(button)
        kb.add(types.InlineKeyboardButton(
            text='Назад', callback_data=f"back_{game.chat_id}"
        ))
        return kb

    def choose_target(self, game, player, targets, index=0):
        kb = types.InlineKeyboardMarkup()
        for target in targets:
            kb.add(types.InlineKeyboardButton(
                text=target.name, callback_data=f"tgt_{game.chat_id}_{target.id}_{index}"
            ))
        kb.add(types.InlineKeyboardButton(
            text='Назад', callback_data=f"back_{game.chat_id}"
        ))
        self.bot.send_message(player.user_id, 'Выбор цели:', reply_markup=kb)

    def choose_act(self, game: TelegramSession, user_id, target_id, act_id):
        player = game.get_player(user_id)
        target = game.get_entity(target_id)
        action = action_manager.get_action(game, player, act_id)
        queue = action_manager.queue_action(game, player, act_id)
        action.target = target

        if action.type == 'item':
            player.items.remove(action.item)

        if queue:
            self.send_act_buttons(player, game)
            return
        player.ready = True
        if not game.unready_players:
            self.cycle(game)

    def process_game_texts(self, game):
        for text in game.texts:
            if not text:
                continue
            for message in text.split('\n\n'):
                self.bot.send_message(game.chat_id, message)
                self.notify_players(game, message)

    def cycle(self, game):
        game.say(f'Ход {game.turn}:')
        game.move()
        self.process_game_texts(game)
        self.pre_move(game.chat_id)

    def send_act_buttons(self, player, game):
        kb = self.get_act_buttons(player, game)
        tts = self.get_act_text(player, game)
        self.bot.send_message(player.user_id, tts, reply_markup=kb)

    def get_act_text(self, player, game):
        attack = action_manager.get_action(game, player, 'attack')

        tts = f"Ход {game.turn}\n" \
              f"{player.hearts}|{player.hp} жизней. Максимум: {player.max_hp}\n" \
              f"{player.energies}|{player.energy} энергии. Максимум: {player.max_energy}\n" \
              f"🎯|Вероятность попасть - {int(attack.hit_chance(player))}%\n"
        if player.weapon.id == 11 and player.weapon.main_target[0]:
            target, power = player.weapon.main_target
            chance = attack.hit_chance(player)
            if power == 1:
                chance += 60
            elif power == 2:
                chance += 90
            tts += f'🎯|Вероятность попасть в {target.name}|🎃 - {chance}%'
        return tts

    def get_skill(self, skill_id, player):
        skills = list(filter(lambda s: s().id == skill_id, modern.all_skills))
        return skills[0]() if skills else Skill()

    def get_weapon(self, weapon_id, player):
        weapons = list(filter(lambda w: w().id == weapon_id, modern.all_weapons))
        return weapons[0]() if weapons else modern.Fist()

    def get_game(self, chat_id) -> TelegramSession:
        chat_id = str(chat_id)
        result = list(filter(lambda s: s.id == chat_id, self.session_manager.sessions))
        if result:
            return result[0]

    def create_game(self, chat_id):
        session = TelegramSession(chat_id)
        self.session_manager.attach_session(session)
        return session

    def join_game(self, chat_id, user_id, user_name):
        game = self.get_game(chat_id)

        player = TelegramEntity(game.id, user_name, user_id)
        player.energy, player.max_energy, player.hp, player.max_hp = 5, 5, 4, 4
        game.entities.append(player)

        self.update_message(game)

    def update_message(self, game):
        tts = f"Игра: {game.name}\n\nУчастники: {', '.join([player.name for player in game.entities])}"
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='♿️Вступить в игру', url=self.bot.get_deep_link(f"jg_{game.chat_id}")))
        kb.add(types.InlineKeyboardButton(text='▶️Запустить игру', callback_data="vd_go"))
        self.bot.edit_message_text(tts, message_id=game.lobby_message.message_id, chat_id=game.lobby_message.chat.id,
                                   reply_markup=kb)

    def choose_items(self, chat_id):
        game = self.get_game(chat_id)
        for player in game.not_chosen_items:
            given = []
            for _ in range(game.items_given):
                item = random.choice(modern.game_items_pool)()
                pool = list(filter(lambda i: i.id not in given, modern.game_items_pool))
                if pool:
                    item = random.choice(pool)()
                given.append(item.id)
                player.items.append(item)
            player.chose_items = True
            if player.npc:
                continue
            self.bot.send_message(player.user_id, f'Ваши предметы: '
                                                  f'{", ".join([item.name for item in player.items])}')

    def choose_weapons(self, chat_id):
        game = self.get_game(chat_id)
        for player in game.not_chosen_weapon:
            if player.npc:
                continue
            self.send_weapon_choice_buttons(player)
        if not game.not_chosen_weapon:
            self.bot.send_message(game.chat_id, f'Оружие выбрано.')
            self.choose_skills(int(chat_id))

    def choose_skills(self, chat_id):
        game = self.get_game(chat_id)
        for player in game.not_chosen_skills:
            if player.npc:
                continue
            self.send_skill_choice_buttons(player)
        if not game.not_chosen_skills:
            weapons_text = '\n'.join([f'{player.name}: {player.weapon.name}' for player in game.alive_entities])
            self.bot.send_message(game.chat_id, f'Способности выбраны, игра начинается! Выбор оружия:\n{weapons_text}')
            self.pre_move(game.chat_id)

    def send_weapon_choice_buttons(self, player, number=3):
        session = self.get_game(player.session_id)

        weapons = []
        for _ in range(number):
            variants = list(filter(lambda w: w.id not in [w.id for w in weapons], modern.all_weapons))
            if not variants:
                break
            choice = random.choice(variants)
            weapons.append(choice())

        kb = types.InlineKeyboardMarkup()
        for weapon in weapons:
            kb.add(types.InlineKeyboardButton(weapon.name, callback_data=f"cw_{session.chat_id}_{weapon.id}"),
                   types.InlineKeyboardButton('Информация', callback_data=f"wi_{weapon.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайное оружие',
                                          callback_data=f"cw_{session.chat_id}_random"))
        self.bot.send_message(player.user_id, 'Выберите оружие:', reply_markup=kb)

    def send_skill_choice_buttons(self, player, number=5, cycle=1):
        game = self.get_game(player.session_id)

        skills = [modern.Inquisitor, modern.Junkie, modern.Scope]
        for _ in range(number):
            variants = list(filter(lambda s: s.id not in [s.id for s in skills], modern.all_skills))
            variants = list(filter(lambda s: s.id not in [s.id for s in player.skills], variants))
            if not variants:
                break
            choice = random.choice(variants)
            skills.append(choice())

        kb = types.InlineKeyboardMarkup()
        for skill in skills:
            kb.add(
                types.InlineKeyboardButton(skill.name, callback_data=f"cs_{cycle}_{game.chat_id}_{skill.id}"),
                types.InlineKeyboardButton('Информация', callback_data=f"ci_{skill.id}"))
        kb.add(types.InlineKeyboardButton(text='Случайный скилл',
                                          callback_data=f"cs_{cycle}_{game.chat_id}_random"))
        self.bot.send_message(player.user_id, f'Выберите скилл ({cycle} из {game.skill_cycles}):', reply_markup=kb)
