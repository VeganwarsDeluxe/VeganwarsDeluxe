from core.Skills.Skill import Skill
from core.Entities.Entity import Entity
import random


class Biceps(Skill):
    id = 'biceps'
    name = 'Бицепс'
    description = 'Даёт шанс нанести удвоенный урон.'

    def __init__(self, source):
        super().__init__(source, stage='attack')

    def register(self):
        @self.source.session.event_manager.every(events='attack')
        def func(message):
            attack = self.source.session.event.action
            if self.source.weapon.ranged:
                return
            if random.randint(0, 100) > 30:
                return
            damage = attack.data.get('damage')
            if not damage:
                return
            self.source.session.say(f'❗️', n=False)
            damage *= 2
            attack.data.update({'damage': damage})
