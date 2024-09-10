from VegansDeluxe.core.Actions.EntityActions import SkipActionGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent, ActionTag
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import PreDamageGameEvent, PostDamageGameEvent
from VegansDeluxe.core import PostActionsGameEvent, PreDamagesGameEvent, PostUpdateActionsGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core.Translator.LocalizedString import ls


class Aflame(State):
    id = 'aflame'

    def __init__(self):
        super().__init__()
        self.flame = 0
        self.dealer = None
        self.extinguished = False

        self.timer = 0

    def add_flame(self, session, entity, dealer, flame):
        self.timer = 2
        self.extinguished = False
        if self.flame == 0:
            session.say(ls("state_aflame_activate").format(entity.name))
        else:
            session.say(ls("state_aflame_increase").format(entity.name))
        self.flame += flame
        self.dealer = dealer


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
        session.say(ls("state_aflame_remove").format(source.name))
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
            action.name = ls("state_aflame_extinguish")

    @RegisterEvent(session.id, event=PreDamagesGameEvent)
    async def handle_pre_damages_event(context: EventContext[PreDamagesGameEvent]):
        """
        Handle events prior to damage calculation.
        """
        if not state.flame:
            return

        if state.extinguished:
            reset_state(state, session, ls("state_aflame_disappear").format(source.name))
            return

        damage = perform_fire_attack(session, source, state, context.event)

        source.inbound_dmg.add(state.dealer, damage, session.turn)
        source.outbound_dmg.add(state.dealer, damage, session.turn)

        if state.flame > 1:
            source.energy -= state.flame - 1
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
        session.say(ls("state_aflame_removing").format(source.name))
        context.event.no_text = True


def reset_state(state, session, message):
    """
    Reset the state to default values and output a message.
    """
    state.flame = 0
    state.extinguished = False
    state.timer = 0
    session.say(message)


def perform_fire_attack(session, source, state, message):
    """
    Perform a fire attack and calculate the damage.
    """
    fire_event = FireAttackGameEvent(message.session_id, message.turn, state.dealer, source, state.flame)
    session.event_manager.publish(fire_event)
    damage = fire_event.damage

    if state.flame == 1:
        session.say(ls("state_aflame_damage").format(source.name, damage))
    elif state.flame > 1:
        session.say(ls("state_aflame_damage_energy").format(source.name, damage, state.flame-1))

    post_fire_event = PostFireAttackGameEvent(message.session_id, message.turn, state.dealer, source, damage)
    session.event_manager.publish(post_fire_event)
    return post_fire_event.damage


class FireAttackGameEvent(PreDamageGameEvent):
    pass


class PostFireAttackGameEvent(PostDamageGameEvent):
    pass
