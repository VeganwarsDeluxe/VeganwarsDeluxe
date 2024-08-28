from VegansDeluxe.core.Actions.ActionTags import ActionTag
from VegansDeluxe.core.Actions.Action import Action
from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Items.Item import Item
from VegansDeluxe.core.Session import Session
from VegansDeluxe.core.Translator.LocalizedString import ls


class ItemAction(Action):
    id = 'item'
    name = ls("base_item_name")

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source)
        self.item = item
        self.tags += [ActionTag.ITEM]
        self.type = 'item'


class FreeItem(ItemAction):
    @property
    def cost(self):
        return False


class DecisiveItem(ItemAction):
    @property
    def cost(self):
        return True
