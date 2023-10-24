from core.Context import Context
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import PreDamagesGameEvent, AttachStateEvent
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
def register(root_context: Context[AttachStateEvent]):
    session: Session = root_context.session
    source = session.get_entity(root_context.event.entity_id)
    state = root_context.event.state

    @RegisterEvent(session.id, event=PreDamagesGameEvent, filters=[lambda e: state.active])
    def func(context: Context[PreDamagesGameEvent]):
        if state.bleeding <= 0:
            session.say(f'🩸|{source.name} теряет ХП от '
                        f'кровотечения! Осталось {source.hp - 1} ХП.')
            source.hp -= 1
            state.active = False
            state.bleeding = 3
            return
        session.say(f'🩸|{source.name} истекает кровью! ({max(state.bleeding, 0)})')
        state.bleeding -= 1
