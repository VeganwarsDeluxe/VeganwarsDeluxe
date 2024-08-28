from VegansDeluxe.core.Actions.Action import Action
from VegansDeluxe.core.Actions.ActionManager import ActionManager
from VegansDeluxe.core.Events.Events import Event, AttachStateEvent, ExecuteActionEvent
from VegansDeluxe.core.Session import Session
from VegansDeluxe.core.States import State


class Context[T]:
    def __init__(self):
        pass


class ActionExecutionContext[T: Action](Context):
    def __init__(self, event: ExecuteActionEvent, session: Session, action_manager: ActionManager):
        super().__init__()
        self.action_manager = action_manager
        self.session_manager = self.action_manager.session_manager
        self.event_manager = self.session_manager.event_manager

        self.event = event
        self.session = session
        self.action: T = event.action


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
