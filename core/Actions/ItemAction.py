from core.Actions.Action import Action
from core.Entities import Entity
from core.Items.Item import Item
from core.Sessions import Session


class ItemAction(Action):
    id = 'item'
    name = 'Item'

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source)
        self.item = item
        self.type = 'item'


class FreeItem(ItemAction):
    @property
    def cost(self):
        return False


class DecisiveItem(ItemAction):
    @property
    def cost(self):
        return True
