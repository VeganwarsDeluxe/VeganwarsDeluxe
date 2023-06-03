import random
from .Weapon import Weapon


class Kastet(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 14
        self.name = 'Кастет'
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

    def attack(self, source, target):
        damage = super().attack(source, target)
        if target.action.id == 'reloading':
            target.say('I lose 4 energies from kastet attack!')
            target.energy -= 4
        return damage
