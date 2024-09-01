from VegansDeluxe.core import Item, FreeItem, AttachedAction, ActionTag
from VegansDeluxe.core import RegisterItem
from VegansDeluxe.core import Allies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Adrenaline(Item):
    id = 'adrenaline'
    name = ls("item_adrenaline_name")


@AttachedAction(Adrenaline)
class AdrenalineAction(FreeItem):
    id = 'adrenaline'
    name = ls("item_adrenaline_name")
    target_type = Allies()
    priority = -2
    
    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    async def func(self, source, target):
        target.energy += 3
        self.session.say(ls("item_adrenaline_text").format(self.source.name, target.name))
