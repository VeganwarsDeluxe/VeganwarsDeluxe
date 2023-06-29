from core.Events.Events import AttackEvent
from core.States.State import State


class Injury(State):
    id = 'injury'

    def __init__(self, source):
        super().__init__(source)
        self.injury = 0

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=AttackEvent)
        def func(message: AttackEvent):
            if not self.injury:
                return
            if message.target != self.source:
                return
            if not message.damage:
                return
            message.damage += self.injury
