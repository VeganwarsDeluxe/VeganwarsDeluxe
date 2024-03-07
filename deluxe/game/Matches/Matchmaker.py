from typing import Optional

from telebot import types

from deluxe.game.Matches.BasicMatch import BasicMatch


# TODO: Refactor


class Matchmaker:
    """Matchmaker Class: Handles matches.."""

    def __init__(self, bot, engine):
        """Initialization function."""
        self.bot = bot
        self.engine = engine

        self.action_manager = self.engine.action_manager
        self.session_manager = self.engine.session_manager
        self.event_manager = self.engine.event_manager

        self.matches: dict[str, BasicMatch] = {}

    def attach_match(self, match: BasicMatch):
        self.matches.update({match.id: match})

    def get_match(self, chat_id) -> Optional[BasicMatch]:
        match = self.matches.get(str(chat_id))
        if not match:
            return
        if not match.session.active:
            del self.matches[match.id]
            return
        return match

    def join_game(self, chat_id, user_id, user_name):
        match = self.get_match(chat_id)
        match.join_session(user_id, user_name)
        self.update_message(match)

    def update_message(self, match: BasicMatch):
        tts = f"Игра: {match.name}\n\nУчастники: {', '.join([player.name for player in match.session.entities])}"
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='♿️Вступить в игру', url=self.bot.get_deep_link(f"jg_{match.id}")))
        kb.add(types.InlineKeyboardButton(text='▶️Запустить игру', callback_data="vd_go"))
        self.bot.edit_message_text(tts, message_id=match.lobby_message.message_id, chat_id=match.lobby_message.chat.id,
                                   reply_markup=kb)
