from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
import random

from core.TargetType import TargetType


class Molot(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 39
        self.name = 'Молот'
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.cooldown_turn = 0
        self.strike = False

    @property
    def actions(self):
        if self.owner.session.turn < self.cooldown_turn or self.owner.energy < 4:
            return super().actions
        return [
            DecisiveAction(self.true_strike, 'Точный удар', 'true_strike', type=TargetType(ally=False, melee=True))
        ] + super().actions

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def true_strike(self, source, target):
        self.cooldown_turn = source.session.turn + 6
        self.owner.energy -= 4
        self.strike = True
        source.session.say(f'🔨|{source.name} наносит точный удар по {target.name}!')
        return self.attack(source, target)
    
    def calculate_damage(self, source, target):
        if not self.strike:
            damage = super().calculate_damage(source, target)
        else:
            damage = self.cubes + self.dmgbonus
        if not damage:
            return damage
        return damage + self.energy_bonus(source)

    def attack(self, source, target):
        return super().attack(source, target)
