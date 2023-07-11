from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import PreMoveGameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from modern.Items.RageSerum import RageSerum


class Alchemist(Skill):
    id = 'alchemist'
    name = 'Алхимик'
    description = 'В начале игры и каждые 9 ходов дает вам сыворотку бешенства, применение ' \
                  'которой заставляет выбранную цель атаковать дополнительно к своему действию..'


@RegisterState(Alchemist)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.every(session.id, turns=9, event=PreMoveGameEvent)
    def func(message: PreMoveGameEvent):
        source.items.append(RageSerum())
