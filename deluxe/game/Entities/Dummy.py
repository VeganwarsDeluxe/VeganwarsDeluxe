import random
from .TelegramEntity import TelegramEntity


class Dummy(TelegramEntity):
    def __init__(self, session_id: str, name):
        super().__init__(session_id, user_name=name, user_id=random.randint(100000000, 99999999999))

        self.npc = True  # to differentiate humans and bots

        self.chose_weapon = True
        self.chose_skills = True
        self.chose_items = False

    @property
    def ready(self):
        return True

    @ready.setter
    def ready(self, value):
        pass

    def choose_act(self, session):
        self.ready = True