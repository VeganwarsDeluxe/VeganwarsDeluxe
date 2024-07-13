from VegansDeluxe.core import Item, FreeItem, AttachedAction, ActionTag, Entity, Everyone
from VegansDeluxe.core import RegisterItem
from VegansDeluxe.core import Allies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Guer(Item):
    id = 'guer'
    name = "Guer"


@AttachedAction(Guer)
class GuerAction(FreeItem):
    id = 'guer'
    name = "Guer"
    target_type = Everyone()
    priority = -2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    def func(self, source: Entity, target: Entity):
        target.hp += 1
        self.session.say(f"💉{target.name} {self.name}!")
