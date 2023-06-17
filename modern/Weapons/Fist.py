from core.Weapons.Weapon import Weapon


class Fist(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 10
        self.accuracybonus = 2
        self.cubes = 2

        self.name = 'Кулаки'
        self.description = 'Ближний бой. Оружие для настоящих боев!'
