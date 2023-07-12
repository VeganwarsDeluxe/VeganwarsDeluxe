from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import MeleeAttack
from core.Weapons.Weapon import MeleeWeapon


class Sword(MeleeWeapon):
    id = 'sword'
    name = 'Меч'
    description = 'Ближний бой, урон 1-3.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 5
        self.damage_bonus = 0


@AttachedAction(Sword)
class SwordAttack(MeleeAttack):
    pass
