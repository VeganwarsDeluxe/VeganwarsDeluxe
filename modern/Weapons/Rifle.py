import random

from core.Action import DecisiveAction
from core.TargetType import Enemies
from core.Weapons.Weapon import Weapon


class Rifle(Weapon):
    id = 'sniperRifle'
    name = 'Снайперская винтовка'
    description = 'Дальний бой, урон 8-8, точность очень низкая. Можно прицелиться вместо атаки,' \
                  ' чтобы повысить точность против выбранного персонажа'

    def __init__(self, source):
        super().__init__(source)
        self.ranged = True
        self.cubes = 1
        self.accuracybonus = -4
        self.energycost = 5
        self.dmgbonus = 7

        self.main_target = None, 0

    @property
    def actions(self):
        return [AimRifle(self.source, self)] + super().actions
    
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


class AimRifle(DecisiveAction):
    id = 'aim_rifle'
    name = 'Выцелить'

    def __init__(self, source, weapon):
        super().__init__(source, Enemies())
        self.weapon = weapon

    def func(self, source, target):
        main_target, level = self.weapon.main_target
        self.weapon.main_target = target, min(2, level + 1)
        source.session.say(f'🎯|{source.name} целится.')
