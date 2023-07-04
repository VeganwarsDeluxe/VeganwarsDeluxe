import random

from core.Events.Events import PostAttackGameEvent
from core.States.State import State


class Armor(State):
    id = 'armor'

    def __init__(self, source):
        super().__init__(source)
        self.armor = []

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=PostAttackGameEvent)
        def func(message: PostAttackGameEvent):
            if message.target == self.source:
                self.negate_damage(message)

    def negate_damage(self, message: PostAttackGameEvent):
        if not message.damage:
            return
        armor = min(message.damage, self.roll_armor())
        if not armor:
            return
        self.session.say(f'🛡|Броня {self.source.name} снимает {armor} урона.')
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
