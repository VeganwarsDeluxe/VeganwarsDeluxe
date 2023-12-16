from core.Context import StateContext, EventContext
from core.Decorators import RegisterState
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from rebuild.States.Armor import Armor
from rebuild.States.DamageThreshold import DamageThreshold


class Cherep(Skill):
    id = 'cherep'
    name = 'Крепкий череп'
    description = 'Ваш порог урона увеличивается (вам сложнее отнять больше, чем одну единицу здоровья), ' \
                  'даёт шанс заблокировать 1 урона.'


@RegisterState(Cherep)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity

    armor = source.get_skill(Armor.id)
    armor.add(1, 50)
    threshold = source.get_skill(DamageThreshold.id)
    threshold.threshold += 1
