from core.Skills.Skill import Skill
from core.Entities.Entity import Entity


class Cherep(Skill):
    def __init__(self, source):
        super().__init__(source, id='cherep', name='Крепкий череп', stage='pre-move')

    def __call__(self, source: Entity):
        if source.session.turn == 1:
            threshold = source.get_skill('damage-threshold')
            threshold.threshold += 1
