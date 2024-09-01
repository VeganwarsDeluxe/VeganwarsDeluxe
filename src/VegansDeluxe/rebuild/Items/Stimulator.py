from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import Item
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Allies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Stimulator(Item):
    id = 'stimulator'
    name = ls("item_stimulator_name")


@AttachedAction(Stimulator)
class StimulatorAction(DecisiveItem):
    id = 'stimulator'
    name = ls("item_stimulator_name")
    target_type = Allies()
    priority = -2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    async def func(self, source, target):
        target.hp = min(target.hp + 2, target.max_hp)
        self.session.say(ls("item_stimulator_text").format(source.name, target.name))
        self.session.say(ls("item_stimulator_effect").format(target.hearts, target.name, target.hp))
