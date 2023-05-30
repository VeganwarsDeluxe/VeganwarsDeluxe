from .Weapon import Weapon


class Tesak(Weapon):
    def __init__(self):
        super().__init__()
        self.id = 61
        self.name = "Тесак"
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0
        self.ranged = False

        self.tesak_bonus = 4
    
    def calculate_damage(self, source, target):
        return super().calculate_damage(source, target) + self.tesak_bonus

    def attack(self, source, target):
        damage = super().attack(source, target)
        if damage:
            self.tesak_bonus = max(self.tesak_bonus-1, 0)
        return damage