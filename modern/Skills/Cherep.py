from core.Events.Events import AttackEvent
from core.Skills.Skill import Skill


class Cherep(Skill):
    id = 'cherep'
    name = 'Крепкий череп'
    description = 'Ваш порог урона увеличивается (вам сложнее отнять больше, чем одну единицу здоровья), ' \
                  'даёт шанс заблокировать 1 урона.'

    def register(self, session_id):
        armor = self.source.get_skill('armor')
        armor.add(1, 50)
        threshold = self.source.get_skill('damage-threshold')
        threshold.threshold += 1
