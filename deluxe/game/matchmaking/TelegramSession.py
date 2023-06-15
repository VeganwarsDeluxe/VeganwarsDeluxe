from core.Sessions.Session import Session
from .TelegramEntity import TelegramEntity


class TelegramSession(Session):
    def __init__(self, chat_id=None):
        super().__init__()
        self.entities: list[TelegramEntity] = []
        self.texts = ['', '']
        self.chat_id = chat_id

        self.lobby = True

        self.skill_cycles = 2
        self.skill_number = 5

    def get_player(self, id):
        result = [p for p in self.entities if p.id == id]
        if result:
            return result[0]

    @property
    def player_ids(self):
        return [p.id for p in self.entities]

    @property
    def unready_players(self):
        return [p for p in self.entities if not p.ready]

    @property
    def not_chosen_weapon(self):
        return [p for p in self.entities if not p.chose_weapon]

    @property
    def not_chosen_skills(self):
        return [p for p in self.entities if not p.chose_skills]

    def say(self, text, n=True):
        self.texts[0] += text + ("\n" if n else '')

    def pre_move(self):
        super().pre_move()
        self.texts = ['', '']
