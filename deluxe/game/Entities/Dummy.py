import random

from core.TargetType import TargetType
from .TelegramEntity import TelegramEntity
import modern
from core.Action import DecisiveAction


class Dummy(TelegramEntity):
    def __init__(self, session, name):
        super().__init__(session, user_name=name, user_id=random.randint(100000000, 99999999999))

        self.npc = True                                   # to differentiate humans and bots

        self.chose_weapon = True
        self.chose_skills = True
        self.chose_items = False

    @property
    def ready(self):
        return True

    @ready.setter
    def ready(self, value):
        pass

    def choose_act(self):
        self.action = DecisiveAction(self.silence, self, TargetType())
        self.ready = True

    def silence(self, source, target):
        pass
