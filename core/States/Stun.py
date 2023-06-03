from core.State import State
from core.Action import DecisiveAction


class Stun(State):
    def __init__(self):
        super().__init__(id='stun', name='Оглушение', constant=True)
        self.stun = 0

    def __call__(self, source):
        if not self.active:
            return
        if source.session.stage == 'pre-move':
            source.actions = self.actions
        if source.session.stage == 'post-damages':
            if self.stun == 1:
                source.say('Я пришел в себя!')
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
            DecisiveAction(self.lay_stun, name='Лежать в стане', id='lay_stun')
        ]


