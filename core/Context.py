from core.Actions.ActionManager import ActionManager
from core.Events.Events import Event, AttachStateEvent
from core.Sessions import Session
from core.States import State


class Context[T]:
    def __init__(self):
        pass


class StateContext[T: State](Context):
    def __init__(self, event: AttachStateEvent, session: Session, action_manager: ActionManager):
        super().__init__()
        self.action_manager = action_manager
        self.session_manager = self.action_manager.session_manager
        self.event_manager = self.session_manager.event_manager

        self.event = event
        self.session = session
        self.state: T = event.state
        self.entity = session.get_entity(event.entity_id)


class EventContext[T: Event](Context):
    def __init__(self, event: T, session: Session, action_manager: ActionManager):
        super().__init__()
        self.action_manager = action_manager
        self.session_manager = self.action_manager.session_manager
        self.event_manager = self.session_manager.event_manager

        self.event: T = event
        self.session = session
