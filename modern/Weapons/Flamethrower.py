import random
from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon, RangedWeapon


class Flamethrower(RangedWeapon):
    id = 'flamethrower'
    name = 'Огнемет'
    description = 'Дальний бой, урон 1-1, точность низкая. Поджигает цель при попадании.'

    def __init__(self):
        super().__init__()
        self.energy_cost = 4
        self.cubes = 1
        self.accuracy_bonus = 2


@AttachedAction(Flamethrower)
class FlamethrowerAttack(Attack):
    def calculate_damage(self, source, target):
        """
        Mostly universal formulas for weapon damage.
        """
        damage = 0
        energy = source.energy + self.accuracybonus if (source.energy > 0) else 0
        cubes = self.cubes - (target.action.id == 'dodge') * 5
        for _ in range(cubes):
            x = random.randint(1, 10)
            if x <= energy:
                damage += 1
        if not damage:
            return 0
        damage += self.dmgbonus
        return 1

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        aflame = target.get_skill('aflame')
        aflame.add_flame(self.session, self.source, source, 1)
        return damage
