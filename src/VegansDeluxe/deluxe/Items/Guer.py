from VegansDeluxe.core import Item, FreeItem, AttachedAction, ActionTag, Entity, Everyone
from VegansDeluxe.core import RegisterItem


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

    tags = FreeItem.tags + [ActionTag.MEDICINE]

    async def func(self, source: Entity, target: Entity):
        target.hp += 1
        self.session.say(f"💉{target.name} {self.name}!")
