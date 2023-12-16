from core.Context import StateContext, EventContext
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import HPLossGameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State


class DamageThreshold(State):
    id = 'damage-threshold'

    def __init__(self):
        super().__init__()
        self.threshold = 6


@RegisterState(DamageThreshold)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    state = root_context.state

    @RegisterEvent(session.id, event=HPLossGameEvent)
    def func(context: EventContext[HPLossGameEvent]):
        if not context.event.damage:
            return
        context.event.hp_loss = (context.event.damage // state.threshold) + 1
