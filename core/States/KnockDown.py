from core.State import State
from core.Action import DecisiveAction


class Knockdown(State):
    def __init__(self):
        super().__init__(id='knockdown', name='Потеря равновесия', constant=True)
        self.active = False

    def __call__(self, source):
        if not self.active:
            return
        if source.session.stage == 'pre-move':
            source.actions.remove(source.get_action('attack'))
            source.actions.remove(source.get_action('dodge'))

    def stand_up(self, source, target):
        self.active = False
        source.say('Я поднялся с земли!')

    @property
    def actions(self):
        if not self.active:
            return []
        return [
            DecisiveAction(self.stand_up, name='Поднятся с земли', id='stand_up')
        ]


