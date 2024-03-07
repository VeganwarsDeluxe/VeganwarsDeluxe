from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


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
