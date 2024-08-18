import random

from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterEvent
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import AttackGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class Biceps(Skill):
    id = 'biceps'
    name = ls("skill_biceps_name")
    description = ls("skill_biceps_description")


@RegisterState(Biceps)
def register(root_context: StateContext[Biceps]):
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
