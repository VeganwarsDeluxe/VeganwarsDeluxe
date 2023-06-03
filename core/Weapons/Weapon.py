import random
from core.Action import DecisiveAction
from core.TargetType import TargetType


class Weapon(object):
    def __init__(self, owner):
        self.id = None
        self.owner = owner
        self.energycost = 2
        self.cubes = 2
        self.dmgbonus = 0
        self.name = 'None'
        self.ranged = False
        self.accuracybonus = 0

    @property
    def actions(self):
        return [DecisiveAction(self.attack, 'Атака', 'attack', type=TargetType(ally=False, melee=not self.ranged))]

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
        source.action.data.update({'damage': damage, 'source': source, 'target': target})
        source.session.trigger('attack')                                   # 7.1 Attack stage
        damage = source.action.data.get('damage')
        target.inbound_dmg += damage
        source.outbound_dmg += damage
        if damage:
            source.session.say(f'👊|{source.name} бьет {target.name} используя {self.name}! Нанесено {damage} урона.')
        else:
            source.session.say(f'💨|{source.name} бьет {target.name} используя {self.name}, но не попадает.')
        return damage
