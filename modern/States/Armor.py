import random
from core.States.State import State


class Armor(State):
    id = 'armor'

    def __init__(self, source):
        super().__init__(source, stage='post-attack')
        self.armor = []

    def __call__(self):
        attack = self.source.session.event.action
        if attack.target == self.source:
            self.negate_damage(attack)

    def negate_damage(self, attack):
        damage = attack.data.get('damage')
        if not damage:
            return
        armor = min(damage, self.roll_armor())
        if not armor:
            return
        self.source.session.say(f'🛡|Броня {self.source.name} снимает {armor} урона.')
        attack.data.update({'damage': damage - armor})

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
