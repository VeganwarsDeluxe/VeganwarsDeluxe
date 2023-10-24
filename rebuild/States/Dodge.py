from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import DecisiveStateAction
from core.Context import Context
from core.Entities import Entity
from core.Events.EventManager import event_manager
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import PostTickGameEvent, GameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State
from core.TargetType import OwnOnly


class Dodge(State):
    id = 'dodge'

    def __init__(self):
        super().__init__()
        self.dodge_cooldown = 0


class DodgeGameEvent(GameEvent):
    def __init__(self, session_id, turn, entity, bonus):
        super().__init__(session_id, turn)
        self.entity = entity
        self.bonus = bonus


@RegisterState(Dodge)
def register(root_context: Context[AttachStateEvent]):
    session: Session = root_context.session
    state = root_context.event.state

    @RegisterEvent(session.id, event=PostTickGameEvent)
    def func(context: Context[PostTickGameEvent]):
        state.dodge_cooldown = max(0, state.dodge_cooldown - 1)


@AttachedAction(Dodge)
class DodgeAction(DecisiveStateAction):
    id = 'dodge'
    name = 'Перекат'
    target_type = OwnOnly()
    priority = -2

    def __init__(self, session: Session, source: Entity, skill: Dodge):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.state.dodge_cooldown != 0

    def func(self, source, target):
        self.state.dodge_cooldown = 5
        bonus = -5
        message = DodgeGameEvent(self.session.id, self.session.turn, source, bonus)
        event_manager.publish(message)
        bonus = message.bonus
        self.source.inbound_accuracy_bonus += bonus
        self.session.say(f"💨|{source.name} перекатывается.")
