from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import PreMoveGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill


class Scope(Skill):
    id = 'scope'
    name = 'Прицел'
    description = 'Повышает точность для дальнобойного оружия на 2.'


@RegisterState(Scope)
def register(root_context: StateContext[Scope]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=PreMoveGameEvent)
    def func(context: EventContext[PreMoveGameEvent]):
        if source.weapon.ranged:
            source.outbound_accuracy_bonus += 2
