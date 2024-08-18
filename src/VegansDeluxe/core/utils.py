import random


def percentage_chance(chance: int):
    return random.randint(1, 100) <= chance


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
