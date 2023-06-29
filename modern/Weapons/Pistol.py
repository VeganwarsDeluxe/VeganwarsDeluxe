from core.Weapons.Weapon import Weapon


class Pistol(Weapon):
    id = 'pistol'
    name = 'Пистолет'
    description = 'Дальний бой, урон 1-3, точность наивысшая.'

    def __init__(self, source):
        super().__init__(source)
        self.ranged = True
        self.cubes = 3
        self.accuracybonus = 3
        self.energycost = 3
