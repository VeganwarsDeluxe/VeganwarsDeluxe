from .Weapon import Weapon


class Fist(Weapon):
    def __init__(self):
        super().__init__()
        self.id = 10
        self.name = 'Кулаки'
        self.accuracybonus = 2
        self.cubes = 2
