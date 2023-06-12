from core.States.State import State


class DamageThreshold(State):
    def __init__(self, source):
        super().__init__(source, id='damage-threshold', name='Покалечен', constant=True)
        self.threshold = 6

    def __call__(self, source):
        if source.session.current_stage != 'hp-loss':
            return
        hp_loss = (source.inbound_dmg.sum() // self.threshold) + 1
        source.cache.update({'hp_loss': hp_loss})



