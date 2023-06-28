from core.Skills.Skill import Skill
from core.Entities.Entity import Entity


class Dvuzhil(Skill):
    id = 'dvuzhil'
    description = 'В начале боя вы получаете +1 хп. Устойчивость к кровотечению повышена.'
    name = 'Двужильность'

    def __init__(self, source):
        super().__init__(source, stage='pre-move')

    def register(self):
        self.source.hp += 1
        self.source.max_hp += 1
