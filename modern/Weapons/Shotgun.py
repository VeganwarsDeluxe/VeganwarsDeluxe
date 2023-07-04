from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon


class Shotgun(Weapon):
    id = 'shotgun'
    name = 'Дробовик'
    description = 'Дальний бой, урон 2-7, точность низкая, затраты энергии: 4. Атакуя цель, находящуюся с ' \
                  'вами в ближнем бою, вы получаете +1 к урону.'

    def __init__(self):
        super().__init__()
        self.energy_cost = 4
        self.damage_bonus = 1
        self.cubes = 6
        self.ranged = True
        self.accuracy_bonus = -2


@AttachedAction(Shotgun)
class ShotgunAttack(Attack):
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if damage == 0:
            return 0
        damage += 1 if target in source.nearby_entities else 0
        return damage
