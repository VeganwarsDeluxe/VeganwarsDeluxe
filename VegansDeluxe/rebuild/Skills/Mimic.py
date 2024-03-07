import random

from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import AttachedAction, Nearest
from VegansDeluxe.core import RegisterEvent, RegisterState
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostUpdateActionsGameEvent, DeliveryRequestEvent, DeliveryPackageEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core import Everyone, Own


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
def register(root_context: StateContext[Mimic]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=PostUpdateActionsGameEvent)
    def post_update_actions(update_context: EventContext[PostUpdateActionsGameEvent]):
        if update_context.event.entity_id != source.id:
            return
        if root_context.state.memorized_action:
            update_context.action_manager.attach_action(session, source, root_context.state.memorized_action)


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
        @Nearest(self.session.id, event=DeliveryPackageEvent)
        def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager

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

        self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))

        self.state.cooldown_turn = self.session.turn + 6


