from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Shotgun(RangedWeapon):
    id = 'shotgun'
    name = ls("weapon_shotgun_name")
    description = ls("weapon_shotgun_description")

    energy_cost = 4
    damage_bonus = 1
    cubes = 6
    accuracy_bonus = -2


@AttachedAction(Shotgun)
class ShotgunAttack(RangedAttack):
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if damage == 0:
            return 0
        damage += 1 if target in source.nearby_entities else 0
        return damage
