from core.Weapons.Weapon import Weapon
import random


class Torch(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 7
        self.accuracybonus = 2
        self.cubes = 3

        self.name = 'Факел'
        self.description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс поджечь цель.'

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        if random.randint(0, 100) > 50:
            aflame = target.get_skill('aflame')
            aflame.add_flame(source, 1)
        return damage

