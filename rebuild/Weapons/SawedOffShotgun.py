from core.ContentManager import AttachedAction, RegisterWeapon
from core.Weapons.Weapon import RangedWeapon
from .Shotgun import ShotgunAttack


@RegisterWeapon
class SawedOffShotgun(RangedWeapon):
    id = 'sawed-off-shotgun'
    name = 'Обрез'
    description = 'Дальний бой, урон 1-4, точность средняя. Атакуя цель, находящуюся с вами в ближнем ' \
                  'бою, вы получаете +1 к урону.'

    energy_cost = 3
    accuracy_bonus = 0
    cubes = 4


@AttachedAction(SawedOffShotgun)
class SawedOffShotgunAttack(ShotgunAttack):
    pass
