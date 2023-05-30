from .Drobovik import Drobovik


class Obrez(Drobovik):
    def __init__(self):
        super().__init__()
        self.id = 4
        self.name = 'Обрез'
        self.energycost = 3
        self.accuracybonus = 0
        self.cubes = 4
        self.ranged = True