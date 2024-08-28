import random

from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import AttachedAction, Next, DeliveryPackageEvent, DeliveryRequestEvent, ActionTag, \
    PreDamagesGameEvent, PostDamagesGameEvent
from VegansDeluxe.core import RegisterEvent, RegisterState, After, At
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PreDeathGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core import Everyone
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.States.Stun import Stun


class Inquisitor(Skill):
    id = 'inquisitor'
    name = ls("skill_inquisitor_name")
    description = ls("skill_inquisitor_description")

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0

        self.random_activated = False


@RegisterState(Inquisitor)
def register(root_context: StateContext[Inquisitor]):
    session: Session = root_context.session
    source = root_context.entity
    state: Inquisitor = root_context.state

    @RegisterEvent(session.id, event=PreDeathGameEvent, priority=2)
    def hp_loss(context: EventContext[PreDeathGameEvent]):
        if context.event.canceled:
            return
        if context.event.entity != source:
            return
        if random.randint(0, 100) > 30:
            return
        if state.random_activated:
            return
        if source.hp <= 0:
            source.hp = 1
            session.say(ls("skill_inquisitor_effect").format(source.name))
            state.random_activated = True
            context.event.canceled = True


@AttachedAction(Inquisitor)
class Pray(DecisiveStateAction):
    id = 'pray'
    name = ls("skill_inquisitor_pray_action_name")
    priority = 2
    target_type = Everyone()

    def __init__(self, session: Session, source: Entity, skill: Inquisitor):
        super().__init__(session, source, skill)
        self.state = skill

        self._timer = 3

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    def func(self, source: Entity, target: Entity):
        self.state.cooldown_turn = self.session.turn + 3
        if source.is_ally(target):
            self.session.say(ls("skill_inquisitor_pray_action_targeted").format(source.name, target.name))

            @At(self.session.id, turn=self.session.turn, event=PreDeathGameEvent)
            def hp_loss(context: EventContext[PreDeathGameEvent]):
                if context.event.entity != source:
                    return
                if source.hp <= 0:
                    source.hp = 1
                    self.session.say(ls("skill_inquisitor_pray_action_saved").format(source.name))
                    context.event.canceled = True

            return

        @Next(self.session.id, event=DeliveryPackageEvent)
        def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager
            harmful_actions = []

            for action in action_manager.get_queued_entity_actions(self.session, target):
                if ActionTag.HARMFUL in action.tags:
                    harmful_actions.append(action)

            if not harmful_actions:
                self.session.say(ls("skill_inquisitor_pray_action_missed").format(source.name, target.name))
                return

            self.session.say(ls("skill_inquisitor_pray_action_angered").format(source.name, target.name))

            @After(self.session.id, turns=0, repeats=2, event=PreDamagesGameEvent)
            def post_actions(actions_context: EventContext[PreDamagesGameEvent]):
                self.session.say(ls("skill_inquisitor_clouds_timer").format(target.name, self.get_timer()))

            @After(self.session.id, turns=3, repeats=1, event=PreDamagesGameEvent)
            def post_actions(actions_context: EventContext[PreDamagesGameEvent]):
                self.session.say(ls("skill_inquisitor_clouds_effect").format(target.name))
                self.session.say(ls("skill_inquisitor_stun").format(target.name))

            @After(self.session.id, turns=3, repeats=1, event=PostDamagesGameEvent)
            def post_actions(actions_context: EventContext[PostDamagesGameEvent]):
                target.get_state(Stun.id).stun += 1

        self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))

    def get_timer(self):
        self._timer -= 1
        return self._timer
