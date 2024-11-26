from VegansDeluxe.core.Actions.Action import Action, FreeAction, DecisiveAction, InstantAction
from VegansDeluxe.core.Actions.ActionTags import ActionTag
from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Items.Item import Item
from VegansDeluxe.core.Session import Session
from VegansDeluxe.core.Translator.LocalizedString import ls


class ItemAction(Action):
    id = 'item'
    name = ls("core.base_item.name")

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source)
        self.item = item
        self.tags += [ActionTag.ITEM]
        self.type = 'item'


class FreeItem(ItemAction, FreeAction):
    pass


class DecisiveItem(ItemAction, DecisiveAction):
    pass


class InstantItem(ItemAction, InstantAction):
    pass
