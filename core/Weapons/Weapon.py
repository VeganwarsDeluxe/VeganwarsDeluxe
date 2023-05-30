import random
from core.Action import DecisiveAction


class Weapon(object):
    def __init__(self):
        self.id = None
        self.energycost = 2
        self.cubes = 2
        self.dmgbonus = 0
        self.name = 'None'
        self.ranged = False
        self.accuracybonus = 0

        self.actions = [
            DecisiveAction(self.attack)
        ]

    def calculate_damage(self, source, target):
        """
        Mostly universal formulas for weapon damage.
        """
        damage = 0
        energy = source.energy + self.accuracybonus if source.energy else 0
        cubes = self.cubes - (target.action.id == 'dodge') * 5
        for _ in range(cubes):
            x = random.randint(1, 10)
            if x <= energy:
                damage += 1
        if not damage:
            return 0
        damage += self.dmgbonus
        return damage

    def attack(self, source, target):
        """
        Actually performs attack on target, dealing damage.
        """
        damage = self.calculate_damage(source, target)
        source.energy -= self.energycost
        target.inbound_dmg += damage
        source.outbound_dmg += damage
        return damage
