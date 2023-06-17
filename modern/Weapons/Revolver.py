import random
from core.Weapons.Weapon import Weapon


class Revolver(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 6
        self.ranged = True
        self.cubes = 3
        self.dmgbonus = 0
        self.energycost = 3
        self.accuracybonus = 2

        self.name = 'Револьвер'
        self.description = 'Дальний бой, урон 3-3, точность средняя.'

    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        return damage if not damage else 3
