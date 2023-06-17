from .Drobovik import Drobovik


class Obrez(Drobovik):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 4
        self.energycost = 3
        self.accuracybonus = 0
        self.cubes = 4
        self.ranged = True

        self.name = 'Обрез'
        self.description = 'Дальний бой, урон 1-4, точность средняя. Атакуя цель, находящуюся с вами в ближнем ' \
                           'бою, вы получаете +1 к урону.'
