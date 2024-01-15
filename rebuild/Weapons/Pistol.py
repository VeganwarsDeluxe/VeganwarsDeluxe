from core.ContentManager import AttachedAction, RegisterWeapon
from core.Actions.WeaponAction import RangedAttack
from core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Pistol(RangedWeapon):
    id = 'pistol'
    name = 'Пистолет'
    description = 'Дальний бой, урон 1-3, точность наивысшая.'

    cubes = 3
    accuracy_bonus = 3
    energy_cost = 3


@AttachedAction(Pistol)
class PistolAttack(RangedAttack):
    pass
