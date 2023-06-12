from core.States.State import State


class Aflame(State):  # TODO: Fix flame lol
    def __init__(self, source):
        super().__init__(source, id='aflame', name='Огонь', constant=True)
        self.flame = 0
        self.extinguished = False

    def __call__(self, source):
        if source.session.current_stage != 'pre-damages':
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
        source.inbound_dmg.add(None, damage)
        if self.flame > 1:
            source.session.say(f'🔥|{source.name} горит. Теряет {self.flame-1} энергии.')
            source.energy -= self.flame-1
        if self.flame == 1:
            self.extinguished = True
        else:
            self.flame -= 1


