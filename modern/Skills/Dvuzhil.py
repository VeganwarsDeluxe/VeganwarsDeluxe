from core.Events.Events import PreMoveEvent
from core.Skills.Skill import Skill


class Dvuzhil(Skill):
    id = 'dvuzhil'
    description = 'В начале боя вы получаете +1 хп. Устойчивость к кровотечению повышена.'
    name = 'Двужильность'

    def register(self, session_id):
        @self.event_manager.at(session_id, turn=1, event=PreMoveEvent)
        def func(message: PreMoveEvent):
            self.source.hp += 1
            self.source.max_hp += 1
