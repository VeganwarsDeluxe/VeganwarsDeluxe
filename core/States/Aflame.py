from core.State import State


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
            source.say('Огонь на мне потух!')
            return
        damage = self.flame
        source.say(f'Я горю. Получаю {damage} урона.')
        source.inbound_dmg += damage
        if self.flame > 1:
            source.say(f'От огня я теряю {self.flame-1} єнергии!')
            source.energy -= self.flame-1
        if self.flame == 1:
            self.extinguished = True
        else:
            self.flame -= 1


