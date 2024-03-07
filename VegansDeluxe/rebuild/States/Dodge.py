from VegansDeluxe.core import AttachedAction
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import Entity

from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import PostTickGameEvent, GameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import OwnOnly


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
def register(root_context: StateContext[Dodge]):
    session: Session = root_context.session
    state = root_context.state

    @RegisterEvent(session.id, event=PostTickGameEvent)
    def func(context: EventContext[PostTickGameEvent]):
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
        self.event_manager.publish(message)
        bonus = message.bonus
        self.source.inbound_accuracy_bonus += bonus
        self.session.say(f"💨|{source.name} перекатывается.")
