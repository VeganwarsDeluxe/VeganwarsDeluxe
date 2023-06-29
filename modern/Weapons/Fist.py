from core.Weapons.Weapon import Weapon


class Fist(Weapon):
    id = 'fist'
    name = 'Кулаки'
    description = 'Ближний бой. Оружие для настоящих боев!'

    def __init__(self, source):
        super().__init__(source)
        self.accuracybonus = 2
        self.cubes = 2
