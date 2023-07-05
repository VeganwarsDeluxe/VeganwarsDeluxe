import random

from core.Entities import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import PostAttackGameEvent, AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.States.State import State


class Armor(State):
    id = 'armor'

    def __init__(self):
        super().__init__()
        self.armor = []

    def negate_damage(self, session: Session, source: Entity, message: PostAttackGameEvent):
        if not message.damage:
            return
        armor = min(message.damage, self.roll_armor())
        if not armor:
            return
        session.say(f'🛡|Броня {source.name} снимает {armor} урона.')
        message.damage -= armor

    def add(self, value: int, chance=100):
        self.armor.append((value, chance))

    def remove(self, armor):
        if armor in self.armor:
            self.armor.remove(armor)

    def roll_armor(self):
        result = 0
        for armor, chance in self.armor:
            for _ in range(armor):
                if random.randint(0, 100) > chance:
                    continue
                result += 1
        return result


@event_manager.at_event(event=AttachStateEvent[Armor])
def register(event):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state = event.state

    @event_manager.at_event(session.id, event=PostAttackGameEvent)
    def func(message: PostAttackGameEvent):
        if message.target == state.source:
            state.negate_damage(session, source, message)
