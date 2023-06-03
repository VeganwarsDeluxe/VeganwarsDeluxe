from core.Weapons.Weapon import Weapon


class Fist(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 10
        self.name = 'Кулаки'
        self.accuracybonus = 2
        self.cubes = 2
