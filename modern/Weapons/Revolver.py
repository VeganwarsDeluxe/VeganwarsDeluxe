from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack, DecisiveWeaponAction
from core.TargetType import OwnOnly
from core.Weapons.Weapon import Weapon, RangedWeapon


class Revolver(RangedWeapon):
    id = 'revolver'
    name = 'Револьвер'
    description = 'Дальний бой, урон 3-3, точность средняя.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.damage_bonus = 0
        self.energy_cost = 3
        self.accuracy_bonus = 2


@AttachedAction(Revolver)
class RevolverAttack(Attack):
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        return damage if not damage else 3


@AttachedAction(Revolver)
class ShootYourself(DecisiveWeaponAction):
    id = 'shoot_yourself'
    name = 'Застрелится'
    priority = 3
    target_type = OwnOnly()

    def func(self, source, target):
        self.session.say(f"🎇|{source.name} застрелился!")
        source.hp = 0
