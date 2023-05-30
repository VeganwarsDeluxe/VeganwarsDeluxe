from .Weapon import Weapon


class Drobovik(Weapon):
    def __init__(self):
        super().__init__()
        self.id = 5
        self.name = 'Дробовик'
        self.energycost = 4
        self.dmgbonus = 1
        self.cubes = 6
        self.ranged = True
        self.accuracybonus = -2
        
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if damage == 0:
            return 0
        damage += 1 if target in source.nearby_entities else 0
        return damage
