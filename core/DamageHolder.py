class DamageHolder:
    def __init__(self):
        self.damages = []

    def add(self, source, damage):
        self.damages.append((source, damage))

    def sum(self):
        total = 0
        for source, damage in self.damages:
            total += damage
        return total

    def clear(self):
        self.damages = []

    def cancel(self, source):
        self.damages = list(filter(lambda d: d[0] != source, self.damages))

    def contributors(self):
        contributors = []
        for source, damage in self.damages:
            if source not in contributors:
                contributors.append(source)
        return contributors

