from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon, RangedWeapon


class Pistol(RangedWeapon):
    id = 'pistol'
    name = 'Пистолет'
    description = 'Дальний бой, урон 1-3, точность наивысшая.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 3
        self.energy_cost = 3


@AttachedAction(Pistol)
class PistolAttack(Attack):
    pass
