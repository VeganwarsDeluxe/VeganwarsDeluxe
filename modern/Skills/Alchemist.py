from core.Events.Events import PreMoveEvent
from core.Skills.Skill import Skill
from modern.Items.RageSerum import RageSerum


class Alchemist(Skill):
    id = 'alchemist'
    name = 'Алхимик'
    description = 'В начале игры и каждые 9 ходов дает вам сыворотку бешенства, применение ' \
                  'которой заставляет выбранную цель атаковать дополнительно к своему действию..'

    def register(self, session_id):
        @self.event_manager.every(session_id, turns=9, event=PreMoveEvent)
        def func(message: PreMoveEvent):
            self.source.items.append(RageSerum(self.source))
