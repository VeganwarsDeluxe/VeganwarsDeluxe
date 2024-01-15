from core.ContentManager import AttachedAction, RegisterItem
from core.Items.Item import Item
from core.Actions.ItemAction import DecisiveItem
from core.TargetType import Enemies


@RegisterItem
class FlashGrenade(Item):
    id = 'flash_grenade'
    name = 'Световая граната'


@AttachedAction(FlashGrenade)
class FlashGrenadeAction(DecisiveItem):
    id = 'flash_grenade'
    name = 'Световая граната'
    target_type = Enemies()
    priority = -1

    def func(self, source, target):
        target.energy = max(0, target.energy - 8)
        self.session.say(f'😵|{self.source.name} кидает световую гранату в {target.name}. (-8 Энергии)')
