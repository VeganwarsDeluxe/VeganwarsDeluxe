from core.Action import DecisiveAction
from core.States.State import State
from core.TargetType import OwnOnly


class Aflame(State):
    id = 'aflame'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.flame = 0
        self.dealer = self.source
        self.extinguished = False

    def __call__(self):
        source = self.source
        if source.session.event.moment == 'post-action':
            if source.action.id == 'skip' and self.flame:
                source.session.say(f'💨|{source.name} потушил себя.')
                self.flame = 0
                self.extinguished = False
        if source.session.event.moment == 'post-update' and self.flame:
            source.remove_action('skip')
        if source.session.event.moment != 'pre-damages':
            return
        if not self.flame:
            return
        if self.extinguished and self.flame == 1:
            self.flame = 0
            self.extinguished = False
            source.session.say(f'🔥|Огонь на {source.name} потух!')
            return
        else:
            self.extinguished = False
        damage = self.flame
        source.session.say(f'🔥|{source.name} горит. Получает {damage} урона.')
        source.inbound_dmg.add(self.dealer, damage)
        source.outbound_dmg.add(self.dealer, damage)
        if self.flame > 1:
            source.session.say(f'🔥|{source.name} горит. Теряет {self.flame - 1} энергии.')
            source.energy -= self.flame - 1
        if self.flame == 1:
            self.extinguished = True
        else:
            self.flame -= 1

    def add_flame(self, source, flame):
        if self.flame == 0:
            source.session.say(f'🔥|{self.source.name} загорелся!')
        else:
            source.session.say(f'🔥|Огонь {self.source.name} усиливается!')
        self.flame += flame
        self.dealer = source

    @property
    def actions(self):
        if not self.flame:
            return []
        return [
            Extinguish(self.source, self)
        ]


class Extinguish(DecisiveAction):
    id = 'extinguish'
    name = 'Потушится'

    def __init__(self, source, state):
        super().__init__(source, OwnOnly())
        self.state = state

    def func(self, source, target):
        self.state.flame = 0
        self.state.extinguished = False
        source.session.say(f'💨|{source.name} тушит себя.')
