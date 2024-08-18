from VegansDeluxe.core import MeleeAttack
import random

from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class BaseballBat(MeleeWeapon):
    id = 'baseball_bat'
    name = ls("weapon_baseball_bat_name")
    description = ls("weapon_baseball_bat_description")

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
        self.session.say(ls("weapon_baseball_bat_effect").format(target.name))
        stun.stun += 2
        return damage
