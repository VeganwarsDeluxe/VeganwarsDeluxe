from .Drobovik import Drobovik


class Obrez(Drobovik):
    id = 'obrez'
    name = 'Обрез'
    description = 'Дальний бой, урон 1-4, точность средняя. Атакуя цель, находящуюся с вами в ближнем ' \
                  'бою, вы получаете +1 к урону.'

    def __init__(self, source):
        super().__init__(source)
        self.energycost = 3
        self.accuracybonus = 0
        self.cubes = 4
        self.ranged = True
