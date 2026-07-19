from VegansDeluxe.core.Object import Object
from VegansDeluxe.core.ObjectTags import ObjectTag
from VegansDeluxe.core.Translator.LocalizedString import ls


class State(Object):
    id = None
    name = ls("core.base_state.name")
    description = ls("core.base_state.description")

    type = 'state'
    tags = Object.tags + [ObjectTag.STATE]