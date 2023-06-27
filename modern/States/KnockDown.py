from core.States.State import State
from core.Action import DecisiveAction
from core.TargetType import TargetType, OwnOnly


class Knockdown(State):
    id = 'knockdown'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.active = False

    def __call__(self):
        source = self.source
        if not self.active:
            return
        if source.session.event.moment == 'post-update':
            source.remove_action('attack')
            source.remove_action('dodge')

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
