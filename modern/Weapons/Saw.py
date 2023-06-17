from core.Weapons.Weapon import Weapon


class Saw(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 28
        self.cubes = 2
        self.accuracybonus = 3
        self.energycost = 3
        self.dmgbonus = 0
        self.ranged = True

        self.name = 'Пиломет'
        self.description = 'Дальний бой, урон 1-1, точность высокая. имеет шанс наложить на цель эффект "ранен", увеличивающий урон от атак по цели на 1.'

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        injury = target.get_skill('injury')
        injury.injury += 1
        source.session.say(f'{target.name} ранен! ({injury.injury})')
        return damage

