from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.EntityActions import SkipActionGameEvent
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.DamageEvents import PreDamageGameEvent, PostDamageGameEvent
from core.Events.EventManager import event_manager, RegisterState
from core.Events.Events import PostActionsGameEvent, PostUpdatesGameEvent, PreDamagesGameEvent, AttachStateEvent, \
    PostUpdateActionsGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State
from core.TargetType import OwnOnly


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
            session.say(f'🔥|{entity.name} загорелся!')
        else:
            session.say(f'🔥|Огонь {entity.name} усиливается!')
        self.flame += flame
        self.dealer = dealer


@RegisterState(Aflame)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state: Aflame = event.state

    @event_manager.at_event(session.id, event=PostActionsGameEvent)
    def handle_post_actions_event(message: PostActionsGameEvent):
        """
        Handle events after actions have been taken.
        """
        if 'skip' not in action_manager.get_queued_entity_actions(session, source) or not state.flame:
            return
        session.say(f'💨|{source.name} потушил себя.')
        state.timer = 0
        state.flame = 0
        state.extinguished = False

    @event_manager.at_event(session.id, event=PostUpdateActionsGameEvent)
    def handle_post_updates_event(message: PostUpdateActionsGameEvent):
        """
        Handle events after updates have been performed.
        """
        if event.entity_id != source.id:
            return
        if state.flame:
            action = action_manager.get_action(session, source, 'skip')
            action.name = 'Потушиться'

    @event_manager.at_event(session.id, event=PreDamagesGameEvent)
    def handle_pre_damages_event(message: PreDamagesGameEvent):
        """
        Handle events prior to damage calculation.
        """
        if not state.flame:
            return

        if state.extinguished:
            reset_state(state, session, f'🔥|Огонь на {source.name} потух!')
            return

        damage = perform_fire_attack(session, source, state, message)

        source.inbound_dmg.add(state.dealer, damage)
        source.outbound_dmg.add(state.dealer, damage)

        if state.flame > 1:
            session.say(f'🔥|{source.name} горит. Теряет {state.flame - 1} энергии.')
            source.energy -= state.flame - 1
        if state.timer <= 1:
            state.extinguished = True
        else:
            state.timer -= 1

    @event_manager.at_event(session.id, event=SkipActionGameEvent)
    def handle_pre_damages_event(message: SkipActionGameEvent):
        """
        Handle skip turn event,
        """
        if message.entity_id != source.id:
            return
        if state.flame == 0:
            return
        state.flame = 0
        state.extinguished = False
        session.say(f'💨|{source.name} тушит себя.')
        message.no_text = True


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
    event_manager.publish(fire_event)
    damage = fire_event.damage

    session.say(f'🔥|{source.name} горит. Получает {damage} урона.')

    post_fire_event = PostFireAttackGameEvent(message.session_id, message.turn, state.dealer, source, damage)
    event_manager.publish(post_fire_event)
    return post_fire_event.damage


class FireAttackGameEvent(PreDamageGameEvent):
    pass


class PostFireAttackGameEvent(PostDamageGameEvent):
    pass