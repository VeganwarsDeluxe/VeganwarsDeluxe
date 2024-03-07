from VegansDeluxe.core import MeleeAttack
import random

from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class BaseballBat(MeleeWeapon):
    id = 'baseball_bat'
    name = 'Бита'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс оглушить цель.'

    accuracy_bonus = 2
    cubes = 3


@AttachedAction(BaseballBat)
class BaseballBatAttack(MeleeAttack):
    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        if random.randint(0, 100) > 30:
            return
        stun = target.get_state('stun')
        self.session.say(f'🌀|{target.name} оглушен!')
        stun.stun += 2
        return damage
