from VegansDeluxe.core import StateContext
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class DoubleVein(Skill):
    id = 'double-vein'
    name = ls("skill_double_vein_name")
    description = ls("skill_double_vein_description")


@RegisterState(DoubleVein)
def register(root_context: StateContext[DoubleVein]):
    session: Session = root_context.session
    source = root_context.entity

    source.hp += 1
    source.max_hp += 1
