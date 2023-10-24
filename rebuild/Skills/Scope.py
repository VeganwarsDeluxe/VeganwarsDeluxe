from core.Context import Context
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import PreMoveGameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Scope(Skill):
    id = 'scope'
    name = 'Прицел'
    description = 'Повышает точность для дальнобойного оружия на 2.'


@RegisterState(Scope)
def register(root_event: Context[AttachStateEvent]):
    session: Session = session_manager.get_session(root_event.event.session_id)
    source = session.get_entity(root_event.event.entity_id)

    @RegisterEvent(session.id, event=PreMoveGameEvent)
    def func(context: Context[PreMoveGameEvent]):
        if source.weapon.ranged:
            source.outbound_accuracy_bonus += 2
