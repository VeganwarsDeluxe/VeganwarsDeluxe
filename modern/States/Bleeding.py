from core.Event import PreDamagesEvent
from core.States.State import State


class Bleeding(State):
    id = 'bleeding'

    def __init__(self, source):
        super().__init__(source)
        self.bleeding = 3
        self.active = False

    def register(self, session_id):
        @self.event_manager.every(session_id, events=PreDamagesEvent)
        def func(message: PreDamagesEvent):
            if not self.active:
                return
            if self.bleeding <= 0:
                self.source.session.say(f'🩸|{self.source.name} теряет ХП от '
                                        f'кровотечения! Осталось {self.source.hp - 1} ХП.')
                self.source.hp -= 1
                self.active = False
                self.bleeding = 3
                return
            self.source.session.say(f'🩸|{self.source.name} истекает кровью! ({self.bleeding})')
            self.bleeding -= 1
