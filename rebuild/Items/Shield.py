from core.ContentManager import AttachedAction, RegisterItem
from core.Actions.ItemAction import DecisiveItem
from core.Context import EventContext
from core.ContentManager import At
from core.Events.DamageEvents import PostDamageGameEvent

from core.Items.Item import Item
from core.TargetType import Allies


@RegisterItem
class Shield(Item):
    id = 'shield'
    name = 'Щит'


@AttachedAction(Shield)
class ShieldAction(DecisiveItem):
    id = 'shield'
    name = 'Щит'
    target_type = Allies()
    priority = -2

    def func(self, source, target):
        if target == source:
            self.session.say(f"🔵|{source.name} использует щит. Урон отражен!")
        else:
            self.session.say(f"🔵|{source.name} использует щит на {target.name}. Урон отражен!")

        @At(self.session.id, turn=self.session.turn, event=PostDamageGameEvent)
        def shield_block(context: EventContext[PostDamageGameEvent]):
            if context.event.target != target:
                return
            if not context.event.damage:
                return
            self.session.say(f"🔵|Щит {source.name} заблокировал весь урон!")
            context.event.damage = 0
