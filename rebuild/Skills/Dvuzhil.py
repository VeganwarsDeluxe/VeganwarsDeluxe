from core.Context import StateContext, EventContext
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
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity

    source.hp += 1
    source.max_hp += 1
