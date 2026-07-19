from VegansDeluxe.core.Object import Object
from VegansDeluxe.core.ObjectTags import ObjectTag
from VegansDeluxe.core.Translator.LocalizedString import ls


class Item(Object):
    id = 'item'
    name = ls("core.base_item.name")

    tags = Object.tags + [ObjectTag.ITEM]
