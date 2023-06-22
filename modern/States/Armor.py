import random
from core.States.State import State


class Armor(State):
    def __init__(self, source):
        super().__init__(source, id='armor', name='Броня', stage='post-attack')
        self.armor = 0

    def __call__(self):
        for entity in self.source.session.entities:
            if entity.action.id != 'attack':
                continue
            if entity.action.data.get('target') == self.source:
                self.negate_damage(entity)

    def negate_damage(self, entity):
        damage = entity.action.data.get('damage')
        if damage == 0:
            return
        armor = min(damage, self.roll_armor())
        if not armor:
            return
        self.source.session.say(f'🛡|Броня {self.source.name} снимает {armor} урона.')
        entity.action.data.update({'damage': damage - armor})

    def add(self, value: int):
        self.armor += value
        if self.armor < 0:
            self.armor = 0

    def roll_armor(self):
        armor = 0
        for _ in range(self.armor):
            if random.randint(0, 100) > 50:
                continue
            armor += 1
        return armor
