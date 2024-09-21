from VegansDeluxe.core import PreMoveGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class Scope(Skill):
    id = 'scope'
    name = ls("rebuild.skill.scope.name")
    description = ls("rebuild.skill.scope.description")


@RegisterState(Scope)
async def register(root_context: StateContext[Scope]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=PreMoveGameEvent)
    async def func(context: EventContext[PreMoveGameEvent]):
        if source.weapon.ranged:
            source.outbound_accuracy_bonus += 2
