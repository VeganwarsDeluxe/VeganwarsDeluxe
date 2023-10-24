import math

from core.Context import Context
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from rebuild.States.Dodge import DodgeGameEvent


class Ninja(Skill):
    id = 'ninja'
    name = 'Ниндзя'
    description = 'По вашему перекату невозможно попасть атакой.'


@RegisterState(Ninja)
def register(root_context: Context[AttachStateEvent]):
    session: Session = session_manager.get_session(root_context.event.session_id)
    source = session.get_entity(root_context.event.entity_id)

    @RegisterEvent(session.id, DodgeGameEvent)
    def pre_actions(context: Context[DodgeGameEvent]):
        if context.event.entity.id != source.id:
            return
        context.event.bonus = -math.inf
