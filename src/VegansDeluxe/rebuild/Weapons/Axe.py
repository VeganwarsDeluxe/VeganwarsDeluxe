from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon
from VegansDeluxe.rebuild.States.DamageThreshold import DamageThreshold


@RegisterWeapon
class Axe(MeleeWeapon):
    id = 'axe'
    name = ls("weapon_axe_name")
    description = ls("weapon_axe_description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0


@AttachedAction(Axe)
class AxeAttack(MeleeAttack):
    def func(self, source, target):
        damage = super().attack(source, target).dealt
        if not damage:
            return damage
        threshold = target.get_state(DamageThreshold.id)
        self.session.say(ls("weapon_axe_effect").format(target.name))

        threshold.threshold -= 1
        return damage
