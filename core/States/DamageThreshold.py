from core.State import State


class DamageThreshold(State):
    def __init__(self):
        super().__init__(id='damage-threshold', name='Покалечен', constant=True)
        self.threshold = 6

    def __call__(self, source):
        if source.session.stage != 'hp-loss':
            return
        hp_loss = (source.inbound_dmg // self.threshold) + 1
        source.cache.update({'hp_loss': hp_loss})



