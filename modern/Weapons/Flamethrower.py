from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import RangedWeapon


class Flamethrower(RangedWeapon):
    id = 'flamethrower'
    name = 'Огнемет'
    description = 'Дальний бой, урон 1-1, точность низкая. Поджигает цель при попадании.'

    def __init__(self):
        super().__init__()
        self.energy_cost = 4
        self.cubes = 2
        self.accuracy_bonus = 2


@AttachedAction(Flamethrower)
class FlamethrowerAttack(Attack):
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if damage:
            return 1

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        aflame = target.get_skill('aflame')
        aflame.add_flame(self.session, self.source, source, 1)
        return damage
