from core.States.State import State


class DamageThreshold(State):
    id = 'damage-threshold'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.threshold = 6

    def register(self):
        @self.source.session.event_manager.every(events=True)
        def func(message):
            source = self.source
            if source.session.event.top != 'hp-loss':
                return
            damage = source.cache.get('hp_loss_damage')
            if not damage:
                return
            hp_loss = (damage // self.threshold) + 1
            source.cache.update({'hp_loss': hp_loss})
