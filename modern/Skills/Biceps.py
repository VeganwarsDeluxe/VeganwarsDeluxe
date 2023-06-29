import random

from core.Events import AttackEvent
from core.Skills.Skill import Skill


class Biceps(Skill):
    id = 'biceps'
    name = 'Бицепс'
    description = 'Даёт шанс нанести удвоенный урон.'

    def register(self, session_id):
        @self.source.session.event_manager.every(event=AttackEvent)
        def func(message: AttackEvent):
            if message.source.weapon.ranged:
                return
            if random.randint(0, 100) > 30:
                return
            if not message.damage:
                return
            self.source.session.say(f'❗️', n=False)
            message.damage *= 2
