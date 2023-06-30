class Weapon:
    id = 'None'
    name = 'None'
    description = 'Описание еще не написано.'

    def __init__(self, energy_cost=2, cubes=2, damage_bonus=0, ranged=False, accuracy_bonus=0):
        self.energy_cost = energy_cost
        self.cubes = cubes
        self.damage_bonus = damage_bonus
        self.ranged = ranged
        self.accuracy_bonus = accuracy_bonus

