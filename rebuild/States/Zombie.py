from core.Context import Context
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import PreDamagesGameEvent, PreDeathGameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State


class ZombieState(State):
    id = 'zombie-state'

    def __init__(self):
        super().__init__()
        self.timer = 0
        self.active = False
        self.deactivations = 0


@RegisterState(ZombieState)
def register(root_context: Context[AttachStateEvent]):
    session: Session = root_context.session
    source = session.get_entity(root_context.event.entity_id)
    state = root_context.event.state

    @RegisterEvent(session.id, event=PreDamagesGameEvent)
    def func(context: Context[PreDamagesGameEvent]):
        if not state.active:
            return
        if state.timer <= 0:
            state.active = False
            state.deactivations += 1
        state.timer -= 1

    @RegisterEvent(session.id, event=PreDeathGameEvent)
    def func(context: Context[PreDeathGameEvent]):
        if context.event.entity != source:
            return
        if state.active:
            context.event.canceled = True
