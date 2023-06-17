from core.Skills.Skill import Skill
from core.Entities.Entity import Entity


class Dvuzhil(Skill):
    def __init__(self, source):
        super().__init__(source, id='dvuzhil', name='Двужильность', stage='pre-move')

    def __call__(self):
        if self.source.session.turn == 1:
            self.source.hp += 1
            self.source.max_hp += 1
