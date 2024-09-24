from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon
from .Shotgun import ShotgunAttack
from ...core.Translator.LocalizedString import ls


@RegisterWeapon
class SawedOffShotgun(RangedWeapon):
    id = 'sawed_off_shotgun'
    name = ls("rebuild.weapon.sawed_off_shotgun.name")
    description = ls("rebuild.weapon.sawed_off_shotgun.description")

    energy_cost = 3
    accuracy_bonus = 0
    cubes = 4


@AttachedAction(SawedOffShotgun)
class SawedOffShotgunAttack(ShotgunAttack):
    pass
