import random

from core.Weapons.Weapon import Weapon


class Flamethrower(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 8
        self.name = 'Огнемет'
        self.ranged = True
        self.energycost = 4
        self.cubes = 1
        self.accuracybonus = 2

    def calculate_damage(self, source, target):
        """
        Mostly universal formulas for weapon damage.
        """
        damage = 0
        energy = source.energy + self.accuracybonus if (source.energy > 0) else 0
        cubes = self.cubes - (target.action.id == 'dodge') * 5
        for _ in range(cubes):
            x = random.randint(1, 10)
            if x <= energy:
                damage += 1
        if not damage:
            return 0
        damage += self.dmgbonus
        return 1

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        aflame = target.get_skill('aflame')
        if aflame.flame == 0:
            source.session.say(f'🔥|{target.name} загорелся!')
        else:
            source.session.say(f'🔥|Огонь {target.name} усиливается!')
        aflame.flame += 1
        aflame.dealer = self.owner
        return damage

