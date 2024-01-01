from core.ContentManager import AttachedAction
from core.Actions.ItemAction import FreeItem
from core.TargetType import Allies
from core.Items.Item import Item


class Adrenaline(Item):
    id = 'adrenaline'
    name = 'Адреналин'


@AttachedAction(Adrenaline)
class AdrenalineAction(FreeItem):
    id = 'adrenaline'
    name = 'Адреналин'
    target_type = Allies()
    priority = -2

    def func(self, source, target):
        target.energy += 3
        self.session.say(f'💉|{self.source.name} использует адреналин на {target.name}! '
                         f'Его енергия увеличена на 3.')
