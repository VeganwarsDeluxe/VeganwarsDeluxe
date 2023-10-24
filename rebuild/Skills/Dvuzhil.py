from core.Context import Context
from core.Decorators import RegisterState
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Dvuzhil(Skill):
    id = 'dvuzhil'
    description = 'В начале боя вы получаете +1 хп. Устойчивость к кровотечению повышена.'
    name = 'Двужильность'


@RegisterState(Dvuzhil)
def register(root_context: Context[AttachStateEvent]):
    session: Session = session_manager.get_session(root_context.event.session_id)
    source = session.get_entity(root_context.event.entity_id)

    source.hp += 1
    source.max_hp += 1
