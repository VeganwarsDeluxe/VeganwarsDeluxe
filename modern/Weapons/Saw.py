from core.Weapons.Weapon import Weapon


class Saw(Weapon):
    id = 28
    name = 'Пиломет'
    description = 'Дальний бой, урон 1-1, точность высокая. имеет шанс наложить на цель эффект "ранен", ' \
                  'увеличивающий урон от атак по цели на 1.'

    def __init__(self, owner):
        super().__init__(owner)
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
        source.session.say(f'{target.name} ранен! ({injury.injury})')
        return damage

