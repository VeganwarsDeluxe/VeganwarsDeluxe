class Weapon:
    id = 'None'
    name = 'None'
    description = 'Описание еще не написано.'
    ranged = False

    def __init__(self, energy_cost=2, cubes=2, damage_bonus=0, accuracy_bonus=0):
        self.energy_cost = energy_cost
        self.cubes = cubes
        self.damage_bonus = damage_bonus
        self.accuracy_bonus = accuracy_bonus


class MeleeWeapon(Weapon):
    ranged = False


class RangedWeapon(Weapon):
    ranged = True
