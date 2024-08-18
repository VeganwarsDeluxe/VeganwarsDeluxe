from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterEvent, RegisterState

from VegansDeluxe.core import PreDeathGameEvent

from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.States.Zombie import ZombieState


class Zombie(Skill):
    id = 'zombie'
    name = ls("skill_zombie_name")
    description = ls("skill_zombie_description")


@RegisterState(Zombie)
def register(root_context: StateContext[Zombie]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=PreDeathGameEvent, priority=3)
    def func(context: EventContext[PreDeathGameEvent]):
        if root_context.event.entity_id != context.event.entity.id:
            return
        if context.event.canceled:
            return
        zombie = source.get_state(ZombieState.id)
        if zombie.active:
            return
        if not zombie.active and zombie.deactivations > 0:
            return
        zombie.active = True
        zombie.timer = 1
        session.say(ls("skill_zombie_effect").format(source.name))
        context.event.canceled = True
