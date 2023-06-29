from core.Events.Events import PreMoveGameEvent
from core.Skills.Skill import Skill


class Dvuzhil(Skill):
    id = 'dvuzhil'
    description = 'В начале боя вы получаете +1 хп. Устойчивость к кровотечению повышена.'
    name = 'Двужильность'

    def register(self, session_id):
        @self.event_manager.at(session_id, turn=1, event=PreMoveGameEvent)
        def func(message: PreMoveGameEvent):
            self.source.hp += 1
            self.source.max_hp += 1
