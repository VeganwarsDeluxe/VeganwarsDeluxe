from core.Weapons.Weapon import Weapon


class Tesak(Weapon):
    id = 'tesak'
    name = "Тесак"
    description = 'Ближний бой, урон 1-3. Имеет изначальный бонус урона 3, за каждое попадание ' \
                  'по цели бонус уменьшается на 1.'

    def __init__(self, source):
        super().__init__(source)
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
            self.tesak_bonus = max(self.tesak_bonus - 1, 0)
        return damage
