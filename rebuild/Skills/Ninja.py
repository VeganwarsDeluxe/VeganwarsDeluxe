import math

from core.ContentManager import RegisterState, RegisterEvent
from core.Context import StateContext, EventContext
from core.Events.Events import AttachStateEvent
from core.Sessions import Session
from core.Skills.Skill import Skill
from rebuild.States.Dodge import DodgeGameEvent


class Ninja(Skill):
    id = 'ninja'
    name = 'Ниндзя'
    description = 'По вашему перекату невозможно попасть атакой.'


@RegisterState(Ninja)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, DodgeGameEvent)
    def pre_actions(context: EventContext[DodgeGameEvent]):
        if context.event.entity.id != source.id:
            return
        context.event.bonus = -math.inf
