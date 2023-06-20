from core.Skills.Skill import Skill
from core.Entities.Entity import Entity


class Cherep(Skill):
    def __init__(self, source):
        super().__init__(source, id='cherep', name='Крепкий череп', stage='pre-move')
        self.description = 'Ваш порог урона увеличивается (вам сложнее отнять больше, чем одну единицу здоровья), ' \
                           'даёт шанс заблокировать 1 урона.'

    def __call__(self):
        if self.source.session.turn == 1:
            threshold = self.source.get_skill('damage-threshold')
            threshold.threshold += 1

            armor = self.source.get_skill('armor')
            armor.add(1)
