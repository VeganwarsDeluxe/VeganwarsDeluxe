from core.Events.EventManager import RegisterState
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from modern.States.Armor import Armor
from modern.States.DamageThreshold import DamageThreshold


class Cherep(Skill):
    id = 'cherep'
    name = 'Крепкий череп'
    description = 'Ваш порог урона увеличивается (вам сложнее отнять больше, чем одну единицу здоровья), ' \
                  'даёт шанс заблокировать 1 урона.'


@RegisterState(Cherep)
def register(event: AttachStateEvent[Cherep]):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    armor = source.get_skill(Armor.id)
    armor.add(1, 50)
    threshold = source.get_skill(DamageThreshold.id)
    threshold.threshold += 1
