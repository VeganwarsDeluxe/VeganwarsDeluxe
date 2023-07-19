import random

from core.Actions.ActionManager import action_manager, AttachedAction
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import AttachStateEvent, PostUpdateActionsGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Everyone, Own


class Mimic(Skill):
    id = 'mimic'
    name = 'Мимик'
    description = 'Если применить эту способность на цель, которая что то делает, вы ' \
                  'получите возможность его повторить!'

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0
        self.memorized_action = None


@RegisterState(Mimic)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.at_event(session.id, event=PostUpdateActionsGameEvent)
    def post_update_actions(update_event: PostUpdateActionsGameEvent):
        if update_event.entity_id != source.id:
            return
        if event.state.memorized_action:
            action_manager.attach_action(session, source, event.state.memorized_action)


@AttachedAction(Mimic)
class CopyAction(DecisiveStateAction):  # TODO: Fix Mimic
    id = 'copyAction'
    name = 'Запомнить действие'
    priority = -2
    target_type = Everyone(own=Own.SELF_EXCLUDED)

    def __init__(self, session: Session, source: Entity, skill: Mimic):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    def func(self, source, target):
        self.state.cooldown_turn = self.session.turn + 6

        action_pool = []
        for action in action_manager.action_queue:
            if action.type == 'item':
                continue
            if action.source != target:
                continue
            action_pool.append(action)

        if not action_pool:
            self.session.say(f'🎭|Мимику {source.name} не удается ничего скопировать у {target.name}!')
            return

        self.session.say(f'🎭|Мимик {source.name} запоминает действие {target.name}!')

        action = random.choice(action_pool)
        self.state.memorized_action = action.id
