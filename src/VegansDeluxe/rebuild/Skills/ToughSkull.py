from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.States.Armor import Armor
from VegansDeluxe.rebuild.States.DamageThreshold import DamageThreshold


class ToughSkull(Skill):
    id = 'tough-skull'
    name = ls("rebuild.skill.tough_skull.name")
    description = ls("rebuild.skill.tough_skull.description")


@RegisterState(ToughSkull)
async def register(root_context: StateContext[ToughSkull]):
    session: Session = root_context.session
    source = root_context.entity

    armor: Armor = source.get_state(Armor.id)
    armor.add(1, 50)
    threshold = source.get_state(DamageThreshold.id)
    threshold.threshold += 1
