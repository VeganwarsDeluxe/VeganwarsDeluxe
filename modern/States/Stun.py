from core.Actions.Action import DecisiveAction
from core.Events.Events import PostUpdatesGameEvent, PostDamagesGameEvent
from core.States.State import State
from core.TargetType import OwnOnly


class Stun(State):
    id = 'stun'

    def __init__(self, source):
        super().__init__(source)
        self.stun = 0

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=PostUpdatesGameEvent)
        def func(message: PostUpdatesGameEvent):
            if not self.active:
                return
            self.source.actions = self.actions

        @self.event_manager.at_event(session_id, event=PostDamagesGameEvent)
        def func(message: PostDamagesGameEvent):
            if not self.active:
                return
            if self.stun == 1:
                self.source.session.say(f'🌀|{self.source.name} приходит в себя.')
            self.stun -= 1

    @property
    def active(self):
        return self.stun

    def lay_stun(self, source, target):
        pass

    @property
    def actions(self):
        if not self.active:
            return []
        return [
            LayStun(self.source)
        ]


class LayStun(DecisiveAction):
    id = 'lay_stun'
    name = 'Лежать в стане'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        pass
