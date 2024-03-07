from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At
from VegansDeluxe.core import PostDamageGameEvent

from VegansDeluxe.core import Item
from VegansDeluxe.core import Allies


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
