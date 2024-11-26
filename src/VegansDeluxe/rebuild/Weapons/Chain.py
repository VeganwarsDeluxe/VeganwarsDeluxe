import random

from VegansDeluxe.core import AttachedAction, Next, RegisterWeapon
from VegansDeluxe.core import DeliveryPackageEvent, DeliveryRequestEvent
from VegansDeluxe.core import Enemies, Distance
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import MeleeAttack, ActionTag
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon
from VegansDeluxe.rebuild import DroppedWeapon


@RegisterWeapon
class Chain(MeleeWeapon):
    id = 'chain'
    name = ls("rebuild.weapon.chain.name")
    description = ls("rebuild.weapon.chain.description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Chain)
class ChainAttack(MeleeAttack):
    pass


@AttachedAction(Chain)
class KnockWeapon(MeleeAttack):
    id = 'knock_weapon'
    name = ls("rebuild.weapon.chain.action.name")
    priority = -1
    target_type = Enemies(distance=Distance.NEARBY_ONLY)

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    async def func(self, source, target):
        @Next(self.session.id, event=DeliveryPackageEvent)
        async def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager

            self.weapon.cooldown_turn = self.session.turn + 6
            damage = (await self.attack(source, target)).dealt
            if not damage:
                self.session.say(ls("rebuild.weapon.chain.action_miss").format(source.name, target.name))
                return

            source_reloading = False
            for action in action_manager.get_queued_entity_actions(self.session, target):
                if ActionTag.RELOAD in action.tags:
                    source_reloading = True

            if source_reloading or random.randint(1, 100) <= 10:
                self.session.say(ls("rebuild.weapon.chain.action.text").format(source.name, target.name))
                state = target.get_state(DroppedWeapon)
                state.drop_weapon(target)
            else:
                self.session.say(ls("rebuild.weapon.chain.action_miss").format(source.name, target.name))

        await self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))
