from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, RangedAttack
from VegansDeluxe.core import OwnOnly
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Revolver(RangedWeapon):
    id = 'revolver'
    name = 'Револьвер'
    description = 'Дальний бой, урон 3-3, точность средняя.'

    cubes = 3
    damage_bonus = 0
    energy_cost = 3
    accuracy_bonus = 2


@AttachedAction(Revolver)
class RevolverAttack(RangedAttack):
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
