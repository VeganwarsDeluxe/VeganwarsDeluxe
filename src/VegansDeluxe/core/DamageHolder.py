class DamageHolder:
    def __init__(self):
        self.damages: list[DamageLog] = []

    def add(self, source, damage: int, turn: int):
        if not damage:
            damage = 0
        self.damages.append(DamageLog(source, damage, turn))

    def sum(self):
        total = 0
        for log in self.damages:
            total += log.damage
        return total

    def clear(self):
        self.damages = []

    def cancel(self, source):
        self.damages = list(filter(lambda d: d.source != source, self.damages))

    def contributors(self):
        contributors = []
        for log in self.damages:
            if log.source not in contributors:
                contributors.append(log.source)
        return contributors


class DamageLog:
    def __init__(self, source, damage: int, turn: int):
        self.source = source
        self.damage = damage
        self.turn = turn
