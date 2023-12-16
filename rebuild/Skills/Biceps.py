import random

from core.Context import StateContext, EventContext
from core.Decorators import RegisterEvent
from core.Decorators import RegisterState
from core.Events.DamageEvents import AttackGameEvent
from core.Events.Events import AttachStateEvent
from core.Sessions import Session
from core.Skills.Skill import Skill


class Biceps(Skill):
    id = 'biceps'
    name = 'Бицепс'
    description = 'Даёт шанс нанести удвоенный урон.'


@RegisterState(Biceps)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session

    @RegisterEvent(session.id, event=AttackGameEvent)
    def func(context: EventContext[AttackGameEvent]):
        if context.event.source.id != root_context.event.entity_id:
            return
        if context.event.source.weapon.ranged:
            return
        if random.randint(0, 100) > 30:
            return
        if not context.event.damage:
            return
        session.say(f'❗️', n=False)
        context.event.damage *= 2
