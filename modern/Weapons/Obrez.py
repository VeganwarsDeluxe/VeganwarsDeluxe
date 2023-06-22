from .Drobovik import Drobovik


class Obrez(Drobovik):
    id = 4
    description = 'Дальний бой, урон 1-4, точность средняя. Атакуя цель, находящуюся с вами в ближнем ' \
                  'бою, вы получаете +1 к урону.'

    def __init__(self, owner):
        super().__init__(owner)
        self.energycost = 3
        self.accuracybonus = 0
        self.cubes = 4
        self.ranged = True

        self.name = 'Обрез'
