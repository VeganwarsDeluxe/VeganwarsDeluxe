from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon
from .Shotgun import ShotgunAttack
from ...core.Translator.LocalizedString import ls


@RegisterWeapon
class SawedOffShotgun(RangedWeapon):
    id = 'sawed-off-shotgun'
    name = ls("weapon_sawed-off-shotgun_name")
    description = ls("weapon_sawed-off-shotgun_description")

    energy_cost = 3
    accuracy_bonus = 0
    cubes = 4


@AttachedAction(SawedOffShotgun)
class SawedOffShotgunAttack(ShotgunAttack):
    pass
