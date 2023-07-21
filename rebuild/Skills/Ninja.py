import math

from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.StateAction import DecisiveStateAction
from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import AttachStateEvent, PostUpdatesGameEvent, PostUpdateActionsGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import OwnOnly


class Ninja(Skill):
    id = 'ninja'
    name = 'Ниндзя'
    description = 'По вашему перекату невозможно попасть атакой.'


@RegisterState(Ninja)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.nearest(session.id, PostUpdateActionsGameEvent)
    def pre_actions(message: PostUpdateActionsGameEvent):
        if message.entity_id != source.id:
            return
        action_manager.remove_action(session, source, 'dodge')


@AttachedAction(Ninja)
class NinjaAction(DecisiveStateAction):
    id = 'dodge'
    name = 'Перекат'
    target_type = OwnOnly()
    priority = -2

    def func(self, source, target):
        target.inbound_accuracy_bonus -= math.inf
        self.session.say(f"💨|{source.name} перекатывается.")
