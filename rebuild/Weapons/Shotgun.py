from core.ContentManager import AttachedAction
from core.Actions.WeaponAction import RangedAttack
from core.Weapons.Weapon import RangedWeapon


class Shotgun(RangedWeapon):
    id = 'shotgun'
    name = 'Дробовик'
    description = 'Дальний бой, урон 2-7, точность низкая, затраты энергии: 4. Атакуя цель, находящуюся с ' \
                  'вами в ближнем бою, вы получаете +1 к урону.'

    energy_cost = 4
    damage_bonus = 1
    cubes = 6
    accuracy_bonus = -2


@AttachedAction(Shotgun)
class ShotgunAttack(RangedAttack):
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if damage == 0:
            return 0
        damage += 1 if target in source.nearby_entities else 0
        return damage
