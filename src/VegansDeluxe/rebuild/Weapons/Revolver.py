from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, RangedAttack
from VegansDeluxe.core import OwnOnly
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Revolver(RangedWeapon):
    id = 'revolver'
    name = ls("rebuild.weapon.revolver.name")
    description = ls("rebuild.weapon.revolver.description")

    cubes = 3
    damage_bonus = 0
    energy_cost = 3
    accuracy_bonus = 2


@AttachedAction(Revolver)
class RevolverAttack(RangedAttack):
    def calculate_damage(self, *args):
        damage = super().calculate_damage(*args)
        return damage if not damage else 3


@AttachedAction(Revolver)
class ShootYourself(DecisiveWeaponAction):
    id = 'shoot_yourself'
    name = ls("rebuild.weapon.revolver_action.name")
    priority = 3
    target_type = OwnOnly()

    async def func(self, source, target):
        self.session.say(ls("rebuild.weapon.revolver_action.text").format(source.name))
        source.hp = 0
