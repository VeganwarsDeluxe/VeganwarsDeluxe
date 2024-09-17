from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostDamageGameEvent
from VegansDeluxe.core import Item
from VegansDeluxe.core import DecisiveItem
import random

from VegansDeluxe.core import Session
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Translator.LocalizedList import LocalizedList
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Grenade(Item):
    id = 'grenade'
    name = ls("item_grenade_name")


@AttachedAction(Grenade)
class GrenadeAction(DecisiveItem):
    id = 'grenade'
    name = ls("item_grenade_name")
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source, item)
        self.tags += [ActionTag.HARMFUL]

        self.damage = 3
        self.range = 2

    async def func(self, source, target):
        damage = self.damage
        targets = []
        for _ in range(self.range):
            target_pool = list(filter(lambda t: t not in targets,
                                      self.get_targets(source, Enemies())
                                      ))
            if not target_pool:
                continue
            target = random.choice(target_pool)
            post_damage = await self.publish_post_damage_event(source, target, damage)
            target.inbound_dmg.add(source, post_damage, self.session.turn)
            source.outbound_dmg.add(source, post_damage, self.session.turn)
            targets.append(target)
        source.energy = max(source.energy - 2, 0)
        self.session.say(
            ls("item_grenade_text")
            .format(source.name, damage, LocalizedList([t.name for t in targets]))
        )

    async def publish_post_damage_event(self, source, target, damage):
        message = PostDamageGameEvent(self.session.id, self.session.turn, source, target, damage)
        await self.event_manager.publish(message)
        return message.damage

    @property
    def blocked(self):
        return self.source.energy < 2
