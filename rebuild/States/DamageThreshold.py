from core.Events.EventManager import event_manager, RegisterState
from core.Events.Events import HPLossGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State


class DamageThreshold(State):
    id = 'damage-threshold'

    def __init__(self):
        super().__init__()
        self.threshold = 6


@RegisterState(DamageThreshold)
def register(event):
    session: Session = session_manager.get_session(event.session_id)
    state = event.state

    @event_manager.at_event(session.id, event=HPLossGameEvent)
    def func(message: HPLossGameEvent):
        if not message.damage:
            return
        message.hp_loss = (message.damage // state.threshold) + 1
