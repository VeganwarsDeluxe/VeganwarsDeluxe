from core.Events.Events import PreMoveGameEvent
from core.Skills.Skill import Skill
from modern.Items.RageSerum import RageSerum


class Alchemist(Skill):
    id = 'alchemist'
    name = 'Алхимик'
    description = 'В начале игры и каждые 9 ходов дает вам сыворотку бешенства, применение ' \
                  'которой заставляет выбранную цель атаковать дополнительно к своему действию..'

    def register(self, session_id):
        @self.event_manager.every(session_id, turns=9, event=PreMoveGameEvent)
        def func(event: PreMoveGameEvent):
            self.source.items.append(RageSerum())
