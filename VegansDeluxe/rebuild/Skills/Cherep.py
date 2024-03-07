from VegansDeluxe.core import StateContext
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.rebuild.States.Armor import Armor
from VegansDeluxe.rebuild.States.DamageThreshold import DamageThreshold


class Cherep(Skill):
    id = 'cherep'
    name = 'Крепкий череп'
    description = 'Ваш порог урона увеличивается (вам сложнее отнять больше, чем одну единицу здоровья), ' \
                  'даёт шанс заблокировать 1 урона.'


@RegisterState(Cherep)
def register(root_context: StateContext[Cherep]):
    session: Session = root_context.session
    source = root_context.entity

    armor = source.get_state(Armor.id)
    armor.add(1, 50)
    threshold = source.get_state(DamageThreshold.id)
    threshold.threshold += 1
