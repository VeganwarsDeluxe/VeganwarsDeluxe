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

    def pick_up(self, source, target):
        source.weapon = self.weapon
        source.session.say(f'🤚{source.name} подбирает потерянное оружие.')
        self.weapon = None

    @property
    def actions(self):
        if not self.active:
            return []
        return [
            DecisiveAction(self.pick_up, self.source, target_type=OwnOnly(), name='Подобрать оружие', id='pick_up')
        ]


