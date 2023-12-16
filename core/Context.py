from core.Events.Events import Event, AttachStateEvent
from core.Sessions import Session
from core.States import State


class Context[T]:
    def __init__(self):
        pass


class StateContext[T: State](Context):
    def __init__(self, event: AttachStateEvent, session: Session):
        super().__init__()

        self.event = event
        self.session = session
        self.state: T = event.state
        self.entity = session.get_entity(event.entity_id)


class EventContext[T: Event](Context):
    def __init__(self, event: T, session: Session):
        super().__init__()

        self.event: T = event
        self.session = session
