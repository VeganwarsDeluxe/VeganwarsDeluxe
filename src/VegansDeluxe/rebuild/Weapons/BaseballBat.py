import random

from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon
from VegansDeluxe.rebuild import Stun


@RegisterWeapon
class BaseballBat(MeleeWeapon):
    id = 'baseball_bat'
    name = ls("rebuild.weapon.baseball_bat.name")
    description = ls("rebuild.weapon.baseball_bat.description")

    accuracy_bonus = 2
    cubes = 3


@AttachedAction(BaseballBat)
class BaseballBatAttack(MeleeAttack):
    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        if not damage:
            return damage
        if random.randint(0, 100) > 30:
            return
        stun = target.get_state(Stun)
        self.session.say(ls("rebuild.weapon.baseball_bat.effect").format(target.name))
        stun.stun += 2
        return damage
