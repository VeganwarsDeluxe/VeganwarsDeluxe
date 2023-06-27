from core.States.State import State
from core.Action import DecisiveAction
from core.TargetType import TargetType, OwnOnly


class KnockedWeapon(State):
    id = 'knocked-weapon'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.weapon = None

    def __call__(self):
        source = self.source
        pass

    @property
    def active(self):
        return self.weapon

    @property
    def actions(self):
        if not self.active:
            return []
        return [
            PickUp(self.source, self)
        ]


class PickUp(DecisiveAction):
    id = 'pick_up'
    name = 'Подобрать оружие'

    def __init__(self, source, state):
        super().__init__(source, OwnOnly())
        self.state = state

    def func(self, source, target):
        source.weapon = self.state.weapon
        source.session.say(f'🤚{source.name} подбирает потерянное оружие.')
        self.state.weapon = None
