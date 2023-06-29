from core.Action import DecisiveAction
from core.Message import PostUpdatesMessage, PostDamagesMessage
from core.States.State import State
from core.TargetType import OwnOnly


class Stun(State):
    id = 'stun'

    def __init__(self, source):
        super().__init__(source)
        self.stun = 0

    def register(self, session_id):
        @self.event_manager.every(session_id, event=PostUpdatesMessage)
        def func(message: PostUpdatesMessage):
            if not self.active:
                return
            self.source.actions = self.actions

        @self.event_manager.every(session_id, event=PostDamagesMessage)
        def func(message: PostDamagesMessage):
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
