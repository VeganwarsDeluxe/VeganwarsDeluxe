from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import AttachStateEvent, HPLossGameEvent, PreDeathGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from rebuild.States.Zombie import ZombieState


class Zombie(Skill):
    id = 'zombie'
    name = 'Зомби'
    description = 'Перед тем, как умереть, вы проживете 2 дополнительных хода.'


@RegisterState(Zombie)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.at_event(session.id, event=PreDeathGameEvent)
    def func(message: PreDeathGameEvent):
        if event.entity_id != message.entity.id:
            return
        zombie = source.get_skill(ZombieState.id)
        if zombie.active:
            return
        if not zombie.active and zombie.deactivations > 0:
            return
        zombie.active = True
        zombie.timer = 1
        session.say(f"😬|{source.name} продолжает сражаться, истекая кровью!")
        message.canceled = True
