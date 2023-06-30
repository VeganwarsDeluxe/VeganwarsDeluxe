from core.Actions.Action import DecisiveAction
from core.Events.Events import PostUpdatesGameEvent
from core.States.State import State
from core.TargetType import OwnOnly


class Knockdown(State):
    id = 'knockdown'

    def __init__(self, source):
        super().__init__(source)
        self.active = False

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=PostUpdatesGameEvent)
        def func(message: PostUpdatesGameEvent):
            if not self.active:
                return
            self.source.remove_action('attack')
            self.source.remove_action('dodge')

    @property
    def actions(self):
        if not self.active:
            return []
        return [
            StandUp(self.source, self)
        ]


class StandUp(DecisiveAction):
    id = 'stand_up'
    name = 'Поднятся с земли'

    def __init__(self, source, state):
        super().__init__(source, OwnOnly())
        self.state = state

    def func(self, source, target):
        self.state.active = False
        source.session.say(f'⬆️|{source.name} поднимается с земли.')
