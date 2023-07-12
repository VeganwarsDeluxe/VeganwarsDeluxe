from core.Events.EventManager import event_manager, RegisterState
from core.Events.Events import PreDamagesGameEvent, PreDeathGameEvent
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
def register(event):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state = event.state

    @event_manager.at_event(session.id, event=PreDamagesGameEvent)
    def func(message: PreDamagesGameEvent):
        if not state.active:
            return
        if state.timer <= 0:
            state.active = False
            state.deactivations += 1
        state.timer -= 1

    @event_manager.at_event(session.id, event=PreDeathGameEvent)
    def func(message: PreDeathGameEvent):
        if message.entity != source:
            return
        if state.active:
            message.canceled = True
