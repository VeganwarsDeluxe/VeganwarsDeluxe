from core.Skills.Skill import Skill
from core.Entities.Entity import Entity


class Cherep(Skill):
    def __init__(self):
        super().__init__(id='cherep', name='Крепкий череп', stage='pre-move')

    def __call__(self, source: Entity):
        if source.session.turn == 0:
            threshold = source.get_skill('damage-threshold')
            threshold.threshold += 1
            source.say('Я получил +1 к порогу урона от крепкого черепа.')
