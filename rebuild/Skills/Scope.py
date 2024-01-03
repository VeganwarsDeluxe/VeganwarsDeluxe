from core.Context import StateContext, EventContext
from core.ContentManager import RegisterState, RegisterEvent
from core.Events.Events import PreMoveGameEvent, AttachStateEvent
from core.Sessions import Session
from core.Skills.Skill import Skill


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
