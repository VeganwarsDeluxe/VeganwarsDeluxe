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
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.at_event(session.id, event=AttackGameEvent)
    def func(message: HPLossGameEvent):
        if source in message.source.inbound_dmg.contributors():
            source.energy += message.hp_loss
            session.say(f'😃|Садист {source.name} получает {message.hp_loss} энергии.')


def get_bonus(session: Session):
    bonus = 0
    for entity in session.entities:
        aflame = entity.get_skill('aflame')
        if aflame.flame:
            bonus += 1
    return bonus
