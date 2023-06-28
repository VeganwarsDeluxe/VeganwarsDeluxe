from core.States.State import State
from core.Action import DecisiveAction
from core.TargetType import TargetType, OwnOnly


class Stun(State):
    id = 'stun'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.stun = 0

    def __call__(self):
        source = self.source
        if not self.active:
            return
        if source.session.event.top == 'post-update':
            source.actions = self.actions
        if source.session.event.top == 'post-damages':
            if self.stun == 1:
                source.session.say(f'🌀|{source.name} приходит в себя.')
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
