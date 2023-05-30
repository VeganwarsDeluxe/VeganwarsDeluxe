from .Entity import Entity
from core.Weapons.Fist import Fist
from core.Action import FreeAction, DecisiveAction, Action


class Dummy(Entity):
    def __init__(self, session, name):
        self.dodge_cooldown = 0

        super().__init__(session)

        self.name = name

        self.hp = 4
        self.max_hp = 4

        self.energy = 5
        self.max_energy = 5

        self.weapon = Fist()

    @property
    def actions(self):
        actions = super().actions
        if self.dodge_cooldown == 0:
            actions += [
                DecisiveAction(self.dodge, 'Перекат', 'dodge')
            ]
        return actions

    def tick_turn(self):
        super().tick_turn()
        self.dodge_cooldown = max(0, self.dodge_cooldown - 1)

    def dodge(self, *args):
        self.dodge_cooldown = 5
        self.say("Dodging!")
