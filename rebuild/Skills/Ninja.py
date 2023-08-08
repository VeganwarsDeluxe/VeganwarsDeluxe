import math

from core.Events.EventManager import RegisterState, event_manager
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
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.at_event(session.id, DodgeGameEvent)
    def pre_actions(message: DodgeGameEvent):
        if message.entity.id != source.id:
            return
        message.bonus = -math.inf
