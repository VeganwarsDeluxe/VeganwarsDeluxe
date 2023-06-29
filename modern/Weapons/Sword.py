from core.Weapons.Weapon import Weapon


class Sword(Weapon):
    id = 'sword'
    name = 'Меч'
    description = 'Ближний бой, урон 1-3.'

    def __init__(self, source):
        super().__init__(source)
        self.name = 'Меч'
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 5
        self.dmgbonus = 0
