from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.StateAction import DecisiveStateAction
from core.Context import StateContext, EventContext
from core.Entities import Entity
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import PostUpdatesGameEvent, PostDamagesGameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State


class Stun(State):
    id = 'stun'

    def __init__(self):
        super().__init__()
        self.stun = 0


@RegisterState(Stun)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PostUpdatesGameEvent)
    def func(context: EventContext[PostUpdatesGameEvent]):
        if not state.stun:
            return
        for action in action_manager.get_actions(session, source):
            if action.id != 'lay_stun':
                action.removed = True

    @RegisterEvent(session.id, event=PostDamagesGameEvent)
    def func(context: EventContext[PostDamagesGameEvent]):
        if not state.stun:
            return
        if state.stun == 1:
            session.say(f'🌀|{source.name} приходит в себя.')
        state.stun -= 1


@AttachedAction(Stun)
class LayStun(DecisiveStateAction):
    id = 'lay_stun'
    name = 'Лежать в стане'

    def __init__(self, session: Session, source: Entity, skill: Stun):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return not self.state.stun

    def func(self, source, target):
        pass
