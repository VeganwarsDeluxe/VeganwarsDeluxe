from core.Events.DamageEvents import AttackGameEvent
from core.Events.EventManager import event_manager, RegisterState
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
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state = event.state

    @event_manager.at_event(session.id, event=AttackGameEvent)
    def func(message: AttackGameEvent):
        if not state.injury:
            return
        if message.target != source:
            return
        if not message.damage:
            return
        message.damage += state.injury
