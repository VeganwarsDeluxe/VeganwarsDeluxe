from core.Actions.WeaponAction import MeleeAttack
from core.ContentManager import AttachedAction
from core.Weapons.Weapon import MeleeWeapon
from rebuild.States.DamageThreshold import DamageThreshold


class Axe(MeleeWeapon):
    id = 'axe'
    name = 'Топор'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс покалечить цель, ' \
                  'после чего ей становится легче снять больше, чем одну жизнь.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0


@AttachedAction(Axe)
class AxeAttack(MeleeAttack):
    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        threshold = target.get_state(DamageThreshold.id)
        self.session.say(f'🤕|{target.name} покалечен!')

        threshold.threshold += 1
        return damage
