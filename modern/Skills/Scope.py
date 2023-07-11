from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import PreMoveGameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from modern.Items.RageSerum import RageSerum


class Scope(Skill):
    id = 'scope'
    name = 'Прицел'
    description = 'Повышает точность для дальнобойного оружия на 2.'


@RegisterState(Scope)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.at_event(session.id, event=PreMoveGameEvent)
    def func(message: PreMoveGameEvent):
        if source.weapon.ranged:
            source.outbound_accuracy_bonus += 2
