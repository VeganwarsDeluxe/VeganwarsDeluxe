from VegansDeluxe.core import PostActionsGameEvent, PreDamagesGameEvent, PostUpdateActionsGameEvent
from VegansDeluxe.core import PreDamageGameEvent, PostDamageGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent, ActionTag
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Actions.EntityActions import SkipActionGameEvent
from VegansDeluxe.core.Translator.LocalizedString import ls


class Aflame(State):
    id = 'aflame'

    def __init__(self):
        super().__init__()
        self.timer = 0
        self.flames = []
        self.dealer = None
        self.extinguished = False

        self.burn_time = 2

    @property
    def flame(self):
        return len(self.flames)

    @flame.setter
    def flame(self, value):
        if value <= 0:
            self.flames = []
            self.dealer = None
            return

        current_flames = len(self.flames)
        if value < current_flames:
            self.flames = self.flames[:value]
        elif value > current_flames:
            if self.dealer is None:
                raise ValueError("Use add_flame() to increase flame with dealer attribution.")
            self.flames.extend([self.dealer] * (value - current_flames))

    def add_flame(self, session, target, source, flame, announce=True):
        self.timer = self.burn_time
        self.extinguished = False
        if announce:
            if self.flame == 0:
                session.say(ls("rebuild.state.aflame.activate").format(target.name))
            else:
                session.say(ls("rebuild.state.aflame.increase").format(target.name))
        self.flames.extend([source] * flame)
        self.dealer = source


@RegisterState(Aflame)
async def register(root_context: StateContext[Aflame]):
    session: Session = root_context.session
    source = root_context.entity
    state: Aflame = root_context.state

    @RegisterEvent(session.id, event=PostActionsGameEvent)
    async def handle_post_actions_event(context: EventContext[PostActionsGameEvent]):
        """
        Handle events after actions have been taken.
        """
        skipped = False
        for action in context.action_manager.get_queued_entity_actions(session, source):
            if ActionTag.SKIP in action.tags:
                skipped = True
                break
        if not skipped or not state.flame:
            return
        session.say(ls("rebuild.state.aflame.remove").format(source.name))
        state.timer = 0
        state.flame = 0
        state.extinguished = False

    @RegisterEvent(session.id, event=PostUpdateActionsGameEvent)
    async def handle_post_updates_event(context: EventContext[PostUpdateActionsGameEvent]):
        """
        Handle events after updates have been performed.
        """
        if root_context.event.entity_id != source.id:
            return
        if state.flame:
            action = context.action_manager.get_action(session, source, 'skip')
            if not action:
                return
            action.name = ls("rebuild.state.aflame.extinguish")

    @RegisterEvent(session.id, event=PreDamagesGameEvent)
    async def handle_pre_damages_event(context: EventContext[PreDamagesGameEvent]):
        """
        Handle events prior to damage calculation.
        """
        if not state.flame:
            return

        if state.extinguished:
            reset_state(state, session, ls("rebuild.state.aflame.disappear").format(source.name))
            return

        fire_attacks = await perform_fire_attacks(session, source, state, context.event)

        for dealer, damage in fire_attacks:
            source.inbound_dmg.add(dealer, damage, session.turn)
            dealer.outbound_dmg.add(source, damage, session.turn)

        if state.flame > 1:
            source.energy = max(0, source.energy - state.flame + 1)
        if state.timer <= 1:
            state.extinguished = True
        else:
            state.timer -= 1

    @RegisterEvent(session.id, event=SkipActionGameEvent)
    async def handle_pre_damages_event(context: EventContext[SkipActionGameEvent]):
        """
        Handle skip turn event,
        """
        if context.event.entity_id != source.id:
            return
        if state.flame == 0:
            return
        state.flame = 0
        state.extinguished = False
        session.say(ls("rebuild.state.aflame.removing").format(source.name))
        context.event.no_text = True


def reset_state(state, session, message):
    """
    Reset the state to default values and output a message.
    """
    state.flame = 0
    state.extinguished = False
    state.timer = 0
    session.say(message)


async def perform_fire_attacks(session: Session, source, state, message):
    """
    Perform fire attacks and calculate the damage for each flame piece.
    """
    fire_attacks = []
    displayed_damage = 0

    for dealer in state.flames:
        fire_event = FireAttackGameEvent(message.session_id, message.turn, dealer, source, 1)
        await session.event_manager.publish(fire_event)
        displayed_damage += fire_event.damage
        fire_attacks.append((dealer, fire_event.damage))

    if state.flame == 1:
        session.say(ls("rebuild.state.aflame.damage").format(source.name, displayed_damage))
    elif state.flame > 1:
        session.say(ls("rebuild.state.aflame.damage_energy").format(source.name, displayed_damage, state.flame-1))

    dealt_fire_attacks = []
    for dealer, damage in fire_attacks:
        post_fire_event = PostFireAttackGameEvent(message.session_id, message.turn, dealer, source, damage)
        await session.event_manager.publish(post_fire_event)
        dealt_fire_attacks.append((dealer, post_fire_event.damage))

    return dealt_fire_attacks


class FireAttackGameEvent(PreDamageGameEvent):
    pass


class PostFireAttackGameEvent(PostDamageGameEvent):
    pass
