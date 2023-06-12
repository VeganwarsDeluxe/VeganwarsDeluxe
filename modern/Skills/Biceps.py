from core.Skills.Skill import Skill
from core.Entities.Entity import Entity
import random


class Biceps(Skill):
    def __init__(self, source):
        super().__init__(source, id='biceps', name='Бицепс', stage='attack')

    @property
    def triggers(self):
        return ['attack']

    def __call__(self, source: Entity):
        if source.weapon.ranged:
            return
        if random.randint(0, 100) > 30:
            return
        damage = source.action.data.get('damage')
        if source != source.action.data.get('source'):
            return
        if damage is None:
            return
        if not damage:
            return
        source.session.say(f'❗️', n=False)
        damage *= 2
        source.action.data.update({'damage': damage})


