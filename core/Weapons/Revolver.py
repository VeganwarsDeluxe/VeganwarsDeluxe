import random
from .Weapon import Weapon


class Revolver(Weapon):
    def __init__(self):
        super().__init__()
        self.id = 6
        self.name = 'Револьвер'
        self.ranged = True
        self.cubes = 3
        self.dmgbonus = 0
        self.energycost = 3
        self.accuracybonus = 2

    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        return damage if not damage else 3
