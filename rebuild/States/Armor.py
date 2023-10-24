import random

from core.Context import Context
from core.Entities import Entity
from core.Events.DamageEvents import PostAttackGameEvent, PostDamageGameEvent
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import AttachStateEvent
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


@RegisterState(Armor)
def register(root_context: Context[AttachStateEvent]):
    session: Session = root_context.session
    source = session.get_entity(root_context.event.entity_id)
    state = root_context.event.state

    @RegisterEvent(session.id, event=PostDamageGameEvent)
    def func(context: Context[PostDamageGameEvent]):
        if context.event.target == source:
            state.negate_damage(session, source, context.event)
