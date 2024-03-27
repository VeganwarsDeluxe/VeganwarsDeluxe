from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At
from VegansDeluxe.core import Item
from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import PostDamagesGameEvent
from VegansDeluxe.core import Everyone
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Chitin(Item):
    id = 'chitin'
    name = ls("item_chitin_name")


@AttachedAction(Chitin)
class ChitinAction(FreeItem):
    id = 'chitin'
    name = ls("item_chitin_name")
    target_type = Everyone()
    priority = -2

    def func(self, source, target):
        target.get_state('armor').add(2, 100)
        self.session.say(ls("item_chitin_text")
                         .format(source.name, target.name))

        @At(self.session.id, turn=self.session.turn + 2, event=PostDamagesGameEvent)
        def chitin_knockout(context: EventContext[PostDamagesGameEvent]):
            target.get_state('armor').remove((2, 100))
            target.get_state('stun').stun += 1
            self.session.say(ls("item_chitin_wear_off").format(target.name))
