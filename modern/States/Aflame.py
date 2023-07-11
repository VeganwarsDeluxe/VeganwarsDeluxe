from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.DamageEvents import PreDamageGameEvent, PostDamageGameEvent
from core.Events.EventManager import event_manager, RegisterState
from core.Events.Events import PostActionsGameEvent, PostUpdatesGameEvent, PreDamagesGameEvent, GameEvent, \
    AttachStateEvent
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

    def add_flame(self, session, source, dealer, flame):
        self.timer = 2
        if self.flame == 0:
            session.say(f'🔥|{source.name} загорелся!')
        else:
            session.say(f'🔥|Огонь {source.name} усиливается!')
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

    @event_manager.at_event(session.id, event=PostUpdatesGameEvent)
    def handle_post_updates_event(message: PostUpdatesGameEvent):
        """
        Handle events after updates have been performed.
        """
        if state.flame:
            action_manager.remove_action(session, source, 'skip')

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


@AttachedAction(Aflame)
class Extinguish(DecisiveStateAction):
    id = 'extinguish'
    name = 'Потушится'
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: Aflame):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return not self.state.flame

    def func(self, source, target):
        self.state.flame = 0
        self.state.extinguished = False
        self.session.say(f'💨|{source.name} тушит себя.')
