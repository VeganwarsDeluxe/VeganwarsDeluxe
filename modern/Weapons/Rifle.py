from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
import random

from core.TargetType import TargetType, Enemies


class Rifle(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 11
        self.name = 'Снайперская винтовка'
        self.ranged = True
        self.cubes = 1
        self.accuracybonus = -4
        self.energycost = 5
        self.dmgbonus = 7

        self.main_target = None, 0

    @property
    def actions(self):
        main_target, level = self.main_target
        if main_target and level == 2:
            return super().actions
        return [DecisiveAction(self.aim_rifle, self.owner,
                               target_type=Enemies(), name='Вьіцелить', id='aim_rifle')] + super().actions

    def aim_rifle(self, source, target):
        main_target, level = self.main_target
        self.main_target = target, min(2, level+1)
        source.session.say(f'🎯|{source.name} целится.')
    
    def calculate_damage(self, source, target):
        main_target, level = self.main_target
        accuracybonus = self.accuracybonus
        if main_target == target:
            accuracybonus = 2 if level == 1 else 5
        damage = 0
        energy = source.energy + accuracybonus if source.energy else 0
        cubes = self.cubes - (target.action.id == 'dodge') * 5
        for _ in range(cubes):
            x = random.randint(1, 10)
            if x <= energy:
                damage += 1
        if not damage:
            return 0
        damage += self.dmgbonus
        return damage

    def attack(self, source, target):
        damage = super().attack(source, target)
        self.main_target = None, 0
        return damage
