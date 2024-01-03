from core.Context import StateContext, EventContext
from core.Events.DamageEvents import AttackGameEvent
from core.ContentManager import RegisterState, RegisterEvent
from core.Events.Events import AttachStateEvent

from core.Sessions import Session
from core.States.State import State


class Injury(State):
    id = 'injury'

    def __init__(self):
        super().__init__()
        self.injury = 0


@RegisterState(Injury)
def register(root_context: StateContext[Injury]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=AttackGameEvent)
    def func(context: EventContext[AttackGameEvent]):
        if not state.injury:
            return
        if context.event.target != source:
            return
        if not context.event.damage:
            return
        context.event.damage += state.injury
