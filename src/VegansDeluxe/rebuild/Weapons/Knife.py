from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon
from VegansDeluxe.rebuild import Bleeding


@RegisterWeapon
class Knife(MeleeWeapon):
    id = 'knife'
    name = ls("rebuild.weapon.knife.name")
    description = ls("rebuild.weapon.knife.description")

    accuracy_bonus = 2
    cubes = 3


@AttachedAction(Knife)
class KnifeAttack(MeleeAttack):
    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        if not damage:
            return damage
        bleeding = target.get_state(Bleeding)
        if bleeding.active:
            bleeding.bleeding -= 1
            self.session.say(ls("rebuild.weapon.knife.increase"))
        else:
            self.session.say(ls("rebuild.weapon.knife.effect").format(target.name))
        bleeding.active = True
        return damage
