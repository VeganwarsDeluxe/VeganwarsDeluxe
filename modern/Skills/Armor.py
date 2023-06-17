from core.Skills.Skill import Skill
from core.Entities.Entity import Entity
import random


class Armor(Skill):
    def __init__(self, source):
        super().__init__(source, id='armor', name='Броня', stage='post-attack')

    def __call__(self):
        if random.randint(0, 100) > 150:
            return
        damage = 0
        entity = self.source
        for entity in self.source.session.entities:
            if entity.action.data.get('target') == self.source:
                damage = entity.action.data.get('damage')
                break
            return
        if entity.action.data.get('armored'):
            return
        entity.action.data.update({'armored': True})
        if damage == 0:
            return
        self.source.session.say(f'🛡|Броня {self.source.name} снимает {1} урона.')
        entity.action.data.update({'damage': damage - 1})
