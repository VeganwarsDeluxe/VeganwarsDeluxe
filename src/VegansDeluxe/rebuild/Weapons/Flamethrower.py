from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon
from VegansDeluxe.rebuild import Aflame


@RegisterWeapon
class Flamethrower(RangedWeapon):
    id = 'flamethrower'
    name = ls("rebuild.weapon.flamethrower.name")
    description = ls("rebuild.weapon.flamethrower.description")

    energy_cost = 3
    cubes = 2
    accuracy_bonus = 2


@AttachedAction(Flamethrower)
class FlamethrowerAttack(RangedAttack):
    def calculate_damage(self, *args):
        damage = super().calculate_damage(*args)
        if damage:
            return 1

    async def func(self, source, target):
        damage = await super().attack(source, target)
        if damage.calculated:
            aflame = target.get_state(Aflame)
            aflame.add_flame(self.session, target, source, 1)
        return damage.dealt
