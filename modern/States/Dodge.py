from core.Actions.Action import DecisiveAction
from core.Events.Events import PostTickGameEvent
from core.States.State import State
from core.TargetType import OwnOnly


class Dodge(State):
    id = 'dodge'

    def __init__(self, source):
        super().__init__(source)
        self.dodge_cooldown = 0

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=PostTickGameEvent)
        def func(message: PostTickGameEvent):
            self.dodge_cooldown = max(0, self.dodge_cooldown - 1)

    @property
    def actions(self):
        if not self.dodge_cooldown == 0:
            return []
        return [
            DodgeAction(self.source, self)
        ]


class DodgeAction(DecisiveAction):
    id = 'dodge'
    name = 'Перекат'

    def __init__(self, source, state):
        super().__init__(source, OwnOnly())
        self.state = state

    def func(self, source, target):
        self.state.dodge_cooldown = 5
        source.session.say(f"💨|{source.name} перекатывается.")
