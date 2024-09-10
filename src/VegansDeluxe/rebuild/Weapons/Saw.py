from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import Next

from VegansDeluxe.core import PostTickGameEvent
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon
from VegansDeluxe.rebuild.States.Injury import Injury


@RegisterWeapon
class Saw(RangedWeapon):
    id = 'saw'
    name = ls("weapon_saw_name")
    description = ls("weapon_saw_description")

    cubes = 2
    accuracy_bonus = 3
    energy_cost = 3
    damage_bonus = 0


@AttachedAction(Saw)
class SawAttack(RangedAttack):
    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        if not damage:
            return damage
        self.session.say(ls("weapon_saw_effect")
                         .format(target.name, target.get_state(Injury.id).injury))

        @Next(self.session.id, PostTickGameEvent)
        def func(context: EventContext[PostTickGameEvent]):
            injury = target.get_state(Injury.id)
            injury.injury += 1

        return damage
