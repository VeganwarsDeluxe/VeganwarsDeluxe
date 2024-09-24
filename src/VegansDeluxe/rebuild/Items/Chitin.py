from VegansDeluxe.core import At
from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import Everyone
from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import Item
from VegansDeluxe.core import PostDamagesGameEvent
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.States.Armor import Armor
from VegansDeluxe.rebuild.States.Stun import Stun


@RegisterItem
class Chitin(Item):
    id = 'chitin'
    name = ls("rebuild.item.chitin.name")


@AttachedAction(Chitin)
class ChitinAction(FreeItem):
    id = 'chitin'
    name = ls("rebuild.item.chitin.name")
    target_type = Everyone()
    priority = -2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    async def func(self, source, target):
        target.get_state(Armor).add(2, 100)
        self.session.say(ls("rebuild.item.chitin.text")
                         .format(source.name, target.name))

        @At(self.session.id, turn=self.session.turn + 2, event=PostDamagesGameEvent)
        async def chitin_knockout(context: EventContext[PostDamagesGameEvent]):
            target.get_state(Armor).remove((2, 100))
            target.get_state(Stun).stun += 1
            self.session.say(ls("rebuild.item.chitin_wear_off").format(target.name))
