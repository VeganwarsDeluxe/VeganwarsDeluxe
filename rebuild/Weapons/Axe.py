from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import MeleeAttack
from core.Weapons.Weapon import MeleeWeapon
from rebuild.States.DamageThreshold import DamageThreshold


class Axe(MeleeWeapon):
    id = 'axe'
    name = 'Топор'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс покалечить цель, ' \
                  'после чего ей становится легче снять больше, чем одну жизнь.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0


@AttachedAction(Axe)
class AxeAttack(MeleeAttack):
    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        threshold = target.get_skill(DamageThreshold.id)
        self.session.say(f'🤕|{target.name} покалечен!')

        threshold.threshold += 1
        return damage
