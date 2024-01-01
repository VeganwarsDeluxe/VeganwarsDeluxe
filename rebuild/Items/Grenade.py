from core.ContentManager import AttachedAction
from core.Entities import Entity
from core.Events.DamageEvents import PostDamageGameEvent
from core.Items.Item import Item
from core.Actions.ItemAction import DecisiveItem
import random

from core.Sessions import Session
from core.TargetType import Enemies


class Grenade(Item):
    id = 'grenade'
    name = 'Граната'


@AttachedAction(Grenade)
class GrenadeAction(DecisiveItem):
    id = 'grenade'
    name = 'Граната'
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source, item)
        self.damage = 3
        self.range = 2

    def func(self, source, target):
        damage = self.damage
        targets = []
        for _ in range(self.range):
            target_pool = list(filter(lambda t: t not in targets,
                                      self.get_targets(source, Enemies())
                                      ))
            if not target_pool:
                continue
            target = random.choice(target_pool)
            post_damage = self.publish_post_damage_event(source, target, damage)
            target.inbound_dmg.add(source, post_damage)
            source.outbound_dmg.add(source, post_damage)
            targets.append(target)
        source.energy = max(source.energy - 2, 0)
        self.session.say(f'💣|{source.name} кидает гранату! Нанесено {damage} урона следующим целям: '
                         f'{",".join([t.name for t in targets])}.')

    def publish_post_damage_event(self, source, target, damage):
        message = PostDamageGameEvent(self.session.id, self.session.turn, source, target, damage)
        self.event_manager.publish(message)
        return message.damage

    @property
    def blocked(self):
        return self.source.energy < 2
