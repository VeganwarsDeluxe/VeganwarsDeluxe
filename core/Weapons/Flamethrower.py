from .Weapon import Weapon


class Flamethrower(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 8
        self.name = 'Огнемет'
        self.ranged = True
        self.energycost = 4
        self.cubes = 2
        self.accuracybonus = 2

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        aflame = target.get_skill('aflame')
        if aflame.flame == 0:
            print(f'{target.name} загорелся!')
        else:
            print(f'Огонь {target.name} усиливается!')
        aflame.flame += 1
        return damage

