from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Knife(MeleeWeapon):
    id = 'knife'
    name = ls("weapon_knife_name")
    description = ls("weapon_knife_description")

    accuracy_bonus = 2
    cubes = 3


@AttachedAction(Knife)
class KnifeAttack(MeleeAttack):
    async def func(self, source, target):
        damage = super().attack(source, target).dealt
        if not damage:
            return damage
        bleeding = target.get_state('bleeding')
        if bleeding.active:
            bleeding.bleeding -= 1
            self.session.say(ls("weapon_knife_increase"))
        else:
            self.session.say(ls("weapon_knife_effect").format(target.name))
        bleeding.active = True
        return damage
