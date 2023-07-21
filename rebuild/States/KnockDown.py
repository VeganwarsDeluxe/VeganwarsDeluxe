from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.EventManager import event_manager, RegisterState
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
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state = event.state

    @event_manager.at_event(session.id, event=PostUpdateActionsGameEvent)
    def func(message: PostUpdateActionsGameEvent):
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
