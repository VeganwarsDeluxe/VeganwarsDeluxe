from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, RangedAttack
from VegansDeluxe.core import OwnOnly
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Revolver(RangedWeapon):
    id = 'revolver'
    name = ls("weapon_revolver_name")
    description = ls("weapon_revolver_description")

    cubes = 3
    damage_bonus = 0
    energy_cost = 3
    accuracy_bonus = 2


@AttachedAction(Revolver)
class RevolverAttack(RangedAttack):
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        return damage if not damage else 3


@AttachedAction(Revolver)
class ShootYourself(DecisiveWeaponAction):
    id = 'shoot_yourself'
    name = ls("weapon_revolver_action_name")
    priority = 3
    target_type = OwnOnly()

    def func(self, source, target):
        self.session.say(ls("weapon_revolver_action_text").format(source.name))
        source.hp = 0
