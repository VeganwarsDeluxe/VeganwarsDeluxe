from core.Context import StateContext, EventContext
from core.ContentManager import RegisterEvent, RegisterState

from core.Events.Events import AttachStateEvent, HPLossGameEvent, PreDeathGameEvent

from core.Sessions import Session
from core.Skills.Skill import Skill
from rebuild.States.Zombie import ZombieState


class Zombie(Skill):
    id = 'zombie'
    name = 'Зомби'
    description = 'Перед тем, как умереть, вы проживете 2 дополнительных хода.'


@RegisterState(Zombie)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=PreDeathGameEvent, priority=3)
    def func(context: EventContext[PreDeathGameEvent]):
        if root_context.event.entity_id != context.event.entity.id:
            return
        if context.event.canceled:
            return
        zombie = source.get_skill(ZombieState.id)
        if zombie.active:
            return
        if not zombie.active and zombie.deactivations > 0:
            return
        zombie.active = True
        zombie.timer = 1
        session.say(f"😬|{source.name} продолжает сражаться, истекая кровью!")
        context.event.canceled = True
