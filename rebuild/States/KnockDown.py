from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.StateAction import DecisiveStateAction
from core.Context import StateContext, EventContext
from core.Entities import Entity
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import PostUpdatesGameEvent, AttachStateEvent, PostUpdateActionsGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State
from core.TargetType import OwnOnly


class Knockdown(State):
    id = 'knockdown'

    def __init__(self):
        super().__init__()
        self.active = False


@RegisterState(Knockdown)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PostUpdateActionsGameEvent)
    def func(context: EventContext[PostUpdateActionsGameEvent]):
        if not state.active:
            return
        action_manager.remove_action(session, source, 'attack')
        action_manager.remove_action(session, source, 'dodge')


@AttachedAction(Knockdown)
class StandUp(DecisiveStateAction):
    id = 'stand_up'
    name = 'Поднятся с земли'
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: Knockdown):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return not self.state.active

    def func(self, source, target):
        self.state.active = False
        self.session.say(f'⬆️|{source.name} поднимается с земли.')
