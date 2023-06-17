from core.Weapons.Weapon import Weapon


class Drobovik(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 5
        self.energycost = 4
        self.dmgbonus = 1
        self.cubes = 6
        self.ranged = True
        self.accuracybonus = -2

        self.name = 'Дробовик'
        self.description = 'Дальний бой, урон 2-7, точность низкая, затраты энергии: 4. Атакуя цель, находящуюся с ' \
                           'вами в ближнем бою, вы получаете +1 к урону.'
        
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if damage == 0:
            return 0
        damage += 1 if target in source.nearby_entities else 0
        return damage