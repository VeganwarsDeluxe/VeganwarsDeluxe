from core.Weapons.Weapon import Weapon
from modern.States.DamageThreshold import DamageThreshold


class Axe(Weapon):
    id = 'axe'
    name = 'Топор'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс покалечить цель, ' \
                  'после чего ей становится легче снять больше, чем одну жизнь.'

    def __init__(self, source):
        super().__init__(source)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        threshold = target.get_skill(DamageThreshold.id)
        source.session.say(f'🤕|{target.name} покалечен!')

        threshold.threshold += 1
        return damage

