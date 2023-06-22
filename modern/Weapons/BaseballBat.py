from core.Weapons.Weapon import Weapon
import random


class BaseballBat(Weapon):
    id = 2
    name = 'Бита'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс оглушить цель.'

    def __init__(self, owner):
        super().__init__(owner)
        self.accuracybonus = 2
        self.cubes = 3

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        if random.randint(0, 100) > 30:
            return
        stun = target.get_skill('stun')
        source.session.say(f'🌀|{target.name} оглушен!')
        stun.stun += 2
        return damage

