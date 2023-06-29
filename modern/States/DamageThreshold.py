from core.Message import HPLossMessage
from core.States.State import State


class DamageThreshold(State):
    id = 'damage-threshold'

    def __init__(self, source):
        super().__init__(source)
        self.threshold = 6

    def register(self, session_id):
        @self.event_manager.every(session_id, event=HPLossMessage)
        def func(message: HPLossMessage):
            if not message.damage:
                return
            message.hp_loss = (message.damage // self.threshold) + 1
