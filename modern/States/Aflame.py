from core.States.State import State


class Aflame(State):
    def __init__(self):
        super().__init__(id='aflame', name='Огонь', constant=True)
        self.flame = 0
        self.extinguished = False

    def __call__(self, source):
        if source.session.stage != 'pre-damages':
            return
        if not self.flame:
            return
        if self.extinguished:
            self.flame = 0
            self.extinguished = False
            source.session.say(f'🔥|Огонь на {source.name} потух!')
            return
        damage = self.flame
        source.session.say(f'🔥|{source.name} горит. Получает {damage} урона.')
        source.inbound_dmg.add(None, damage)
        if self.flame > 1:
            source.session.say(f'🔥|{source.name} горит. Теряет {self.flame-1} энергии.')
            source.energy -= self.flame-1
        if self.flame == 1:
            self.extinguished = True
        else:
            self.flame -= 1


