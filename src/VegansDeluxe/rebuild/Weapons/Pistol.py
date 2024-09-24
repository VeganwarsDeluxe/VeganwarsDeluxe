from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Pistol(RangedWeapon):
    id = 'pistol'
    name = ls("rebuild.weapon.pistol.name")
    description = ls("rebuild.weapon.pistol.description")

    cubes = 3
    accuracy_bonus = 3
    energy_cost = 3


@AttachedAction(Pistol)
class PistolAttack(RangedAttack):
    pass
