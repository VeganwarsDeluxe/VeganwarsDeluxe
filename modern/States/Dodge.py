from core.States.State import State
from core.Action import DecisiveAction
from core.TargetType import TargetType, OwnOnly


class Dodge(State):
    id = 'dodge'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.dodge_cooldown = 0

    def __call__(self):
        source = self.source
        if source.session.event.moment == 'post-tick':
            self.dodge_cooldown = max(0, self.dodge_cooldown - 1)

    def dodge(self, source, target):
        self.dodge_cooldown = 5
        source.session.say(f"💨|{source.name} перекатывается.")

    @property
    def actions(self):
        if not self.dodge_cooldown == 0:
            return []
        return [
            DecisiveAction(self.dodge, self.source, target_type=OwnOnly(), name='Перекат', id='dodge')
        ]


