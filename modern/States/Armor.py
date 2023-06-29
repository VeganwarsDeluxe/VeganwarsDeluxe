import random

from core.Message import PostAttackMessage
from core.States.State import State


class Armor(State):
    id = 'armor'

    def __init__(self, source):
        super().__init__(source)
        self.armor = []

    def register(self, session_id):
        @self.event_manager.every(session_id, event=PostAttackMessage)
        def func(message: PostAttackMessage):
            if message.target == self.source:
                self.negate_damage(message)

    def negate_damage(self, message: PostAttackMessage):
        if not message.damage:
            return
        armor = min(message.damage, self.roll_armor())
        if not armor:
            return
        self.source.session.say(f'🛡|Броня {self.source.name} снимает {armor} урона.')
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
