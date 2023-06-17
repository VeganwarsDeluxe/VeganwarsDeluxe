from core.Skills.Skill import Skill
from core.Entities.Entity import Entity
import random


class Biceps(Skill):
    def __init__(self, source):
        super().__init__(source, id='biceps', name='Бицепс', stage='attack')

    @property
    def triggers(self):
        return ['attack']

    def __call__(self):
        if self.source.weapon.ranged:
            return
        if random.randint(0, 100) > 30:
            return
        damage = self.source.action.data.get('damage')
        if not damage:
            return
        self.source.session.say(f'❗️', n=False)
        damage *= 2
        self.source.action.data.update({'damage': damage})


