from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At

from VegansDeluxe.core import Item
from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import PostDamagesGameEvent, PreMoveGameEvent
from VegansDeluxe.core import Allies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Jet(Item):
    id = 'jet'
    name = ls("item_jet_name")


@AttachedAction(Jet)
class JetAction(FreeItem):
    id = 'jet'
    name = ls("item_jet_name")
    target_type = Allies()

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    async def func(self, source, target):
        self.session.say(
            ls("item_jet_text").format(source.name, target.name)
        )

        @At(self.session.id, turn=self.session.turn + 2, event=PostDamagesGameEvent, priority=3)
        async def jet_reload(context: EventContext[PostDamagesGameEvent]):
            self.session.say(
                ls("item_jet_effect").format(target.name, target.max_energy)
            )

        @At(self.session.id, turn=self.session.turn + 3, event=PreMoveGameEvent, priority=3)
        async def jet_reload(context: EventContext[PreMoveGameEvent]):
            target.energy = target.max_energy
