from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import Item
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class FlashGrenade(Item):
    id = 'flash_grenade'
    name = ls("item_flash_grenade_name")


@AttachedAction(FlashGrenade)
class FlashGrenadeAction(DecisiveItem):
    id = 'flash_grenade'
    name = ls("item_flash_grenade_name")
    target_type = Enemies()
    priority = -1

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.HARMFUL]

    def func(self, source, target):
        target.energy = max(0, target.energy - 8)
        self.session.say(ls("item_flash_grenade_text").format(self.source.name, target.name))
