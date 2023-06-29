from core.Action import DecisiveAction
from core.TargetType import OwnOnly
from core.Weapons.Weapon import Weapon


class Revolver(Weapon):
    id = 'revolver'
    name = 'Револьвер'
    description = 'Дальний бой, урон 3-3, точность средняя.'

    def __init__(self, owner):
        super().__init__(owner)
        self.ranged = True
        self.cubes = 3
        self.dmgbonus = 0
        self.energycost = 3
        self.accuracybonus = 2

    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        return damage if not damage else 3

    @property
    def actions(self):
        return [
            ShootYourself(self.source, self)
        ] + super().actions


class ShootYourself(DecisiveAction):
    id = 'shoot_yourself'
    name = 'Застрелится'

    def __init__(self, source, weapon):
        super().__init__(source, OwnOnly(), priority=3)
        self.weapon = weapon

    def func(self, source, target):
        source.session.say(f"🎇|{source.name} застрелился!")
        source.hp = 0
