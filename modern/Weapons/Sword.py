from core.Weapons.Weapon import Weapon


class Sword(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 30
        self.name = 'Меч'
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 5
        self.dmgbonus = 0

        self.name = 'Меч'
        self.description = 'Ближний бой, урон 1-3.'
