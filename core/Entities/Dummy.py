from .Entity import Entity
from modern.Weapons.Fist import Fist
from core.Action import DecisiveAction
from core.TargetType import OwnOnly


class Dummy(Entity):
    def __init__(self, session, name):
        self.dodge_cooldown = 0

        super().__init__(session)

        self.name = name

        self.hp = 4
        self.max_hp = 4

        self.energy = 5
        self.max_energy = 5

        self.weapon = Fist(self)

    @property
    def default_actions(self):
        actions = super().default_actions
        if self.dodge_cooldown == 0:
            actions += [
                DecisiveAction(self.dodge, self, target_type=OwnOnly(), name='Перекат', id='dodge')
            ]
        return actions

    def tick_turn(self):
        super().tick_turn()
        self.dodge_cooldown = max(0, self.dodge_cooldown - 1)

    def dodge(self, *args):
        self.dodge_cooldown = 5
        self.session.say(f"💨|{self.name} перекатывается.")
