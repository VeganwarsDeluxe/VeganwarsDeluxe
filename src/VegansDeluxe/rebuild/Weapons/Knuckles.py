from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import MeleeAttack, ActionTag
from VegansDeluxe.core import Next
from VegansDeluxe.core import PreDamagesGameEvent
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Knuckles(MeleeWeapon):
    id = 'knuckles'
    name = ls("rebuild.weapon.knuckles.name")
    description = ls("rebuild.weapon.knuckles.description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0


@AttachedAction(Knuckles)
class KnucklesAttack(MeleeAttack):
    priority = -1

    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        if not damage:
            return damage

        @Next(self.session.id, event=PreDamagesGameEvent)
        async def pre_damages(context: EventContext[PreDamagesGameEvent]):
            reloading = False
            for action in context.action_manager.get_queued_entity_actions(self.session, target):
                if ActionTag.RELOAD in action.tags:
                    reloading = True
            if reloading:
                self.session.say(ls("rebuild.weapon.knuckles.effect").format(target.name))
                target.energy = max(target.energy - 4, 0)

        return damage
