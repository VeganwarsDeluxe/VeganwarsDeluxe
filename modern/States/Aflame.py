from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.EventManager import event_manager
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


@event_manager.at_event(event=AttachStateEvent[Aflame])
def register(event: AttachStateEvent[Aflame]):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state = event.state

    @event_manager.at_event(session.id, event=PostActionsGameEvent)
    def func(message: PostActionsGameEvent):
        if source.action.id == 'skip' and state.flame:
            session.say(f'💨|{source.name} потушил себя.')
            state.timer = 0
            state.flame = 0
            state.extinguished = False

    @event_manager.at_event(session.id, event=PostUpdatesGameEvent)
    def func(message: PostUpdatesGameEvent):
        if not state.flame:
            return
        source.remove_action('skip')

    @event_manager.at_event(session.id, event=PreDamagesGameEvent)
    def func(message: PreDamagesGameEvent):
        if not state.flame:
            return
        if state.extinguished:
            state.flame = 0
            state.extinguished = False
            state.timer = 0
            session.say(f'🔥|Огонь на {source.name} потух!')
            return
        else:
            state.extinguished = False
        damage = state.flame

        message = FireAttackGameEvent(message.session_id, message.turn, state.dealer, source, damage)
        event_manager.publish(message)
        damage = message.damage

        session.say(f'🔥|{source.name} горит. Получает {damage} урона.')

        message = PostFireAttackGameEvent(message.session_id, message.turn, state.dealer, source, damage)
        event_manager.publish(message)
        damage = message.damage

        source.inbound_dmg.add(state.dealer, damage)
        source.outbound_dmg.add(state.dealer, damage)
        if state.flame > 1:
            session.say(f'🔥|{source.name} горит. Теряет {state.flame - 1} энергии.')
            source.energy -= state.flame - 1
        if state.timer <= 1:
            state.extinguished = True
        else:
            state.timer -= 1


class FireAttackGameEvent(GameEvent):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PostFireAttackGameEvent(GameEvent):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


@AttachedAction(Aflame)
class Steal(DecisiveStateAction):
    id = 'extinguish'
    name = 'Потушится'
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: Aflame):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return not self.flame

    def func(self, source, target):
        self.state.flame = 0
        self.state.extinguished = False
        self.session.say(f'💨|{source.name} тушит себя.')
