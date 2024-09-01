import math

from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.States.Dodge import DodgeGameEvent


class Ninja(Skill):
    id = 'ninja'
    name = ls("skill_ninja_name")
    description = ls("skill_ninja_description")


@RegisterState(Ninja)
async def register(root_context: StateContext[Ninja]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, DodgeGameEvent)
    async def pre_actions(context: EventContext[DodgeGameEvent]):
        if context.event.entity.id != source.id:
            return
        context.event.bonus = -math.inf
