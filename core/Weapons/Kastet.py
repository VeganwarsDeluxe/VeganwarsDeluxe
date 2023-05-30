import random
from .Weapon import Weapon


class Kastet(Weapon):
    def __init__(self):
        super().__init__()
        self.id = 14
        self.name = 'Кастет'
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

    def attack(self, source, target):
        damage = super().attack(source, target)
        if target.current_action == 'reloading':
            target.say('I lose 4 energies from kastet attack!')
            target.energy -= 4
        return damage
