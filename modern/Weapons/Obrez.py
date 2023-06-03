from .Drobovik import Drobovik


class Obrez(Drobovik):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 4
        self.name = 'Обрез'
        self.energycost = 3
        self.accuracybonus = 0
        self.cubes = 4
        self.ranged = True