from .Entity import Entity
from core.Weapons.Fist import Fist
from core.Action import FreeAction, DecisiveAction, Action


class Player(Entity):
    def __init__(self, session, name):
        super().__init__(session)

        self.name = name

        self.hp = 4
        self.max_hp = 4

        self.energy = 5
        self.max_energy = 5

        self.weapon = Fist()

        self.dodge_cooldown = 0

        self.actions += [
            DecisiveAction(self.dodge, 'Перекат', 'dodge')
        ]

    @property
    def targets(self):
        return self.nearby_entities if not self.weapon.ranged else \
            [entity for entity in self.session.entities if entity != self]

    def tick_turn(self):
        super().tick_turn()
        self.dodge_cooldown = max(0, self.dodge_cooldown - 1)

    def dodge(self, *args):
        self.dodge_cooldown = 5
        self.say("Dodging!")
