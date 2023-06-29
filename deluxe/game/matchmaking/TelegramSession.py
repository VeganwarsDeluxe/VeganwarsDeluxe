from core.Sessions.Session import Session
from deluxe.game.Entities.TelegramEntity import TelegramEntity


class TelegramSession(Session):
    name = 'Basic'

    def __init__(self, chat_id=None):
        super().__init__()
        self.entities: list[TelegramEntity] = []
        self.texts = ['', '']

        self.chat_id = chat_id
        self.lobby_message = None
        self.lobby = True

        self.skill_cycles = 2
        self.skill_number = 5

        self.items_given = 2
        self.cowed = False

    def get_player(self, user_id):
        result = [p for p in self.entities if p.id == user_id]
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

    @property
    def not_chosen_items(self):
        return [p for p in self.entities if not p.chose_items]

    def say(self, text, n=True):
        self.texts[0] += text + ("\n" if n else '')

    def pre_move(self):
        super().pre_move()
        self.texts = ['', '']
