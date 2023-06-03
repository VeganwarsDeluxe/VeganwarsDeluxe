from core.Weapons.Weapon import Weapon


class Pistol(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 1
        self.name = 'Пистолет'
        self.ranged = True
        self.cubes = 3
        self.accuracybonus = 3
        self.energycost = 3