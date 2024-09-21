from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Police(MeleeWeapon):
    id = 'police_bat'
    name = ls("rebuild.weapon.police_bat.name")
    description = ls("rebuild.weapon.police_bat.description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0


@AttachedAction(Police)
class PoliceAttack(MeleeAttack):
    priority = -1

    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        if not damage:
            return damage
        target.energy = max(target.energy - 1, 0)
        self.session.say(ls("rebuild.weapon.police_bat.effect").format(target.name))
        return damage
