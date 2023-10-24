from core.Context import Context
from core.Decorators import RegisterEvent
from core.Events.DamageEvents import AttackGameEvent
from core.Events.EventManager import event_manager
from core.Events.Events import AttachStateEvent, HPLossGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Pyromaniac(Skill):
    id = 'pyromaniac'
    name = 'Пиромант'
    description = 'За каждого горящего соперника вы получаете бонус к урону.'


# @RegisterState(Pyromaniac)
def register(root_context: Context[AttachStateEvent]):
    session: Session = session_manager.get_session(root_context.event.session_id)
    source = session.get_entity(root_context.event.entity_id)

    @RegisterEvent(session.id, event=HPLossGameEvent)
    def func(context: Context[HPLossGameEvent]):
        if source in context.event.source.inbound_dmg.contributors():
            source.energy += context.event.hp_loss
            session.say(f'😃|Садист {source.name} получает {context.event.hp_loss} энергии.')


def get_bonus(session: Session):
    bonus = 0
    for entity in session.entities:
        aflame = entity.get_skill('aflame')
        if aflame.flame:
            bonus += 1
    return bonus
