from core.Context import Context
from core.Events.DamageEvents import AttackGameEvent
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State


class Injury(State):
    id = 'injury'

    def __init__(self):
        super().__init__()
        self.injury = 0


@RegisterState(Injury)
def register(root_context: Context[AttachStateEvent]):
    session: Session = root_context.session
    source = session.get_entity(root_context.event.entity_id)
    state = root_context.event.state

    @RegisterEvent(session.id, event=AttackGameEvent)
    def func(context: Context[AttackGameEvent]):
        if not state.injury:
            return
        if context.event.target != source:
            return
        if not context.event.damage:
            return
        context.event.damage += state.injury
