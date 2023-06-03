from .Weapon import Weapon


class Saw(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 28
        self.name = 'Пиломет'
        self.cubes = 2
        self.accuracybonus = 3
        self.energycost = 3
        self.dmgbonus = 0
        self.ranged = True

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        injury = target.get_skill('injury')
        injury.injury += 1
        print(f'{target.name} ранен! ({injury.injury})')
        return damage

