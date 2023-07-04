from core.Skills.Skill import Skill
from modern import Armor, DamageThreshold


class Cherep(Skill):
    id = 'cherep'
    name = 'Крепкий череп'
    description = 'Ваш порог урона увеличивается (вам сложнее отнять больше, чем одну единицу здоровья), ' \
                  'даёт шанс заблокировать 1 урона.'

    def register(self, session_id):
        armor = self.source.get_skill(Armor.id)
        armor.add(1, 50)
        threshold = self.source.get_skill(DamageThreshold.id)
        threshold.threshold += 1
