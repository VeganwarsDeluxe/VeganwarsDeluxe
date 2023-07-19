from core.Events.EventManager import event_manager, RegisterState
from core.Events.Events import PreDamagesGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State


class Bleeding(State):
    id = 'bleeding'

    def __init__(self):
        super().__init__()
        self.bleeding = 3
        self.active = False


@RegisterState(Bleeding)
def register(event):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state = event.state

    @event_manager.at_event(session.id, event=PreDamagesGameEvent)
    def func(message: PreDamagesGameEvent):
        if not state.active:
            return
        if state.bleeding <= 0:
            session.say(f'🩸|{source.name} теряет ХП от '
                        f'кровотечения! Осталось {source.hp - 1} ХП.')
            source.hp -= 1
            state.active = False
            state.bleeding = 3
            return
        session.say(f'🩸|{source.name} истекает кровью! ({max(state.bleeding, 0)})')
        state.bleeding -= 1
