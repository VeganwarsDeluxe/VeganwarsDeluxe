from VegansDeluxe.core import Allies
from VegansDeluxe.core import At
from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import Item
from VegansDeluxe.core import PostDamageGameEvent
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Shield(Item):
    id = 'shield'
    name = ls("rebuild.item.shield.name")


@AttachedAction(Shield)
class ShieldAction(DecisiveItem):
    id = 'shield'
    name = ls("rebuild.item.shield.name")
    target_type = Allies()
    priority = -2

    async def func(self, source, target):
        if target == source:
            self.session.say(ls("rebuild.item.shield.text").format(source.name))
        else:
            self.session.say(ls("rebuild.item.shield.text_targeted").format(source.name, target.name))

        @At(self.session.id, turn=self.session.turn, event=PostDamageGameEvent)
        async def shield_block(context: EventContext[PostDamageGameEvent]):
            if context.event.target != target:
                return
            if not context.event.damage:
                return
            context.event.damage = 0
