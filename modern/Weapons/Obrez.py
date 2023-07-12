from core.Actions.ActionManager import AttachedAction
from core.Weapons.Weapon import RangedWeapon
from .Shotgun import ShotgunAttack


class Obrez(RangedWeapon):
    id = 'obrez'
    name = 'Обрез'
    description = 'Дальний бой, урон 1-4, точность средняя. Атакуя цель, находящуюся с вами в ближнем ' \
                  'бою, вы получаете +1 к урону.'

    def __init__(self):
        super().__init__()
        self.energy_cost = 3
        self.accuracy_bonus = 0
        self.cubes = 4


@AttachedAction(Obrez)
class ObrezAttack(ShotgunAttack):
    pass
