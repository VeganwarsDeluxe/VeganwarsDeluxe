from core.Weapons.Weapon import Weapon


class Fist(Weapon):
    id = 10
    description = 'Ближний бой. Оружие для настоящих боев!'

    def __init__(self, owner):
        super().__init__(owner)
        self.accuracybonus = 2
        self.cubes = 2

        self.name = 'Кулаки'
