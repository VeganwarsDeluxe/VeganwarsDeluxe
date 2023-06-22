from core.Weapons.Weapon import Weapon
import random


class Torch(Weapon):
    id = 7
    name = 'Факел'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс поджечь цель.'

    def __init__(self, owner):
        super().__init__(owner)
        self.accuracybonus = 2
        self.cubes = 3

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        if random.randint(0, 100) > 50:
            aflame = target.get_skill('aflame')
            aflame.add_flame(source, 1)
        return damage

