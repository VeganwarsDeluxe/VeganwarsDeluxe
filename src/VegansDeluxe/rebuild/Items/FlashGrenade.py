from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Enemies
from VegansDeluxe.core import Item
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class FlashGrenade(Item):
    id = 'flash_grenade'
    name = ls("rebuild.item.flash_grenade.name")


@AttachedAction(FlashGrenade)
class FlashGrenadeAction(DecisiveItem):
    id = 'flash_grenade'
    name = ls("rebuild.item.flash_grenade.name")
    target_type = Enemies()
    priority = -1

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.HARMFUL]

    async def func(self, source, target):
        target.energy = max(0, target.energy - 8)
        self.session.say(ls("rebuild.item.flash_grenade.text").format(self.source.name, target.name))
