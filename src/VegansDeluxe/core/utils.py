import math
import random


def percentage_chance(chance: int) -> bool:
    return random.randint(1, 100) <= chance

def per_cubes(cubes: int, accuracy: int, energy=0, entity_accuracies=0, critical=False) -> int:
    total_accuracy = (accuracy + entity_accuracies + energy)
    result = sum(1 for _ in range(cubes) if random.randint(1, 10) <= total_accuracy)
    if critical and total_accuracy > 10:
        damage = int(math.floor(result * total_accuracy / 10))
    return result



class MatrixIndexCounter:
    def __init__(self, width: int):
        self.width = max(width-1, 1)

        self.row = 0
        self.column = 0

    def current(self):
        return self.row, self.column

    def next(self):
        if self.column == self.width:
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        return self.current()

    def reset(self, width: int = None):
        if width:
            self.width = max(width-1, 1)
        self.row = 0
        self.column = 0
