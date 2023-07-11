import random

from core.Events.EventManager import RegisterState, event_manager
from core.Events.DamageEvents import AttackGameEvent
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Biceps(Skill):
    id = 'biceps'
    name = 'Бицепс'
    description = 'Даёт шанс нанести удвоенный урон.'


@RegisterState(Biceps)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)

    @event_manager.at_event(session.id, event=AttackGameEvent)
    def func(message: AttackGameEvent):
        if message.source.weapon.ranged:
            return
        if random.randint(0, 100) > 30:
            return
        if not message.damage:
            return
        session.say(f'❗️', n=False)
        message.damage *= 2
