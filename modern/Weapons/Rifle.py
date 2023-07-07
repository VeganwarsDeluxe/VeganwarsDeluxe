import random

from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import DecisiveWeaponAction, Attack
from core.Entities import Entity
from core.Sessions import Session
from core.TargetType import Enemies
from core.Weapons.Weapon import Weapon, RangedWeapon


class Rifle(RangedWeapon):
    id = 'sniperRifle'
    name = 'Снайперская винтовка'
    description = 'Дальний бой, урон 8-8, точность очень низкая. Можно прицелиться вместо атаки,' \
                  ' чтобы повысить точность против выбранного персонажа'

    def __init__(self):
        super().__init__()
        self.cubes = 1
        self.accuracy_bonus = -4
        self.energy_cost = 5
        self.damage_bonus = 7

        self.main_target = None, 0


@AttachedAction(Rifle)
class RifleAttack(Attack):
    def __init__(self, session: Session, source: Entity, weapon: Rifle):
        super().__init__(session, source, weapon)
        self.weapon: Rifle = weapon

    def calculate_damage(self, source, target):
        main_target, level = self.weapon.main_target
        if main_target == target:
            self.weapon.accuracy_bonus = 2 if level == 1 else 5
        else:
            self.weapon.accuracy_bonus = -4
        return super().calculate_damage(source, target)

    def attack(self, source, target):
        damage = super().attack(source, target)
        self.weapon.main_target = None, 0
        return damage


@AttachedAction(Rifle)
class AimRifle(DecisiveWeaponAction):
    id = 'aim_rifle'
    name = 'Выцелить'
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Rifle):
        super().__init__(session, source, weapon)
        self.weapon: Rifle = weapon

    def func(self, source, target):
        main_target, level = self.weapon.main_target
        self.weapon.main_target = target, min(2, level + 1)
        self.session.say(f'🎯|{source.name} целится.')
