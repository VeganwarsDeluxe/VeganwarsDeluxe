from VegansDeluxe.core import Item, FreeItem, AttachedAction, ActionTag, Entity, Everyone
from VegansDeluxe.core import RegisterItem
from VegansDeluxe.core import Allies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Nuir(Item):
    id = 'nuir'
    name = "Nuir"


@AttachedAction(Nuir)
class NuirAction(FreeItem):
    id = 'nuir'
    name = "Nuir"
    target_type = Everyone()
    priority = -2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    async def func(self, source: Entity, target: Entity):
        target.hp -= 1
        self.session.say(f"💉{target.name} {self.name}!")
