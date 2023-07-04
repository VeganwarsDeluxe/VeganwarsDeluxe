import random

from core.Events.Events import AttackGameEvent
from core.Skills.Skill import Skill


class Biceps(Skill):
    id = 'biceps'
    name = 'Бицепс'
    description = 'Даёт шанс нанести удвоенный урон.'

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=AttackGameEvent)
        def func(message: AttackGameEvent):
            if message.source.weapon.ranged:
                return
            if random.randint(0, 100) > 30:
                return
            if not message.damage:
                return
            self.session.say(f'❗️', n=False)
            message.damage *= 2
