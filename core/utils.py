import random


def percentage_chance(chance: int):
    return random.randint(1, 100) <= chance
