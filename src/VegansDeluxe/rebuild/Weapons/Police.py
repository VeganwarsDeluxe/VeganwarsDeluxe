from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Police(MeleeWeapon):
    id = 'police_bat'
    name = ls("weapon_police_bat_name")
    description = ls("weapon_police_bat_description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0


@AttachedAction(Police)
class PoliceAttack(MeleeAttack):
    priority = -1

    async def func(self, source, target):
        damage = super().attack(source, target).dealt
        if not damage:
            return damage
        target.energy = max(target.energy - 1, 0)
        self.session.say(ls("weapon_police_bat_effect").format(target.name))
        return damage
