import random
from core.Action import DecisiveAction
from core.TargetType import Enemies


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
        return [
            DecisiveAction(self.attack, 'Атака', 'attack', type=Enemies(distance=not self.ranged))
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

        source.action.data.update({'damage': damage, 'source': source, 'target': target})
        source.session.trigger('attack')                                   # 7.1 Pre-Attack stage
        damage = source.action.data.get('damage')

        self.attack_text(source, target, damage)

        source.action.data.update({'damage': damage, 'source': source, 'target': target})
        source.session.trigger('post-attack')  # 7.2 Post-Attack stage
        damage = source.action.data.get('damage')

        target.inbound_dmg.add(source, damage)
        source.outbound_dmg.add(target, damage)
        return damage

    def attack_text(self, source, target, damage):
        attack_text = 'стреляет' if self.ranged else 'бьет'
        attack_emoji = '💥' if self.ranged else '👊'
        if damage:
            source.session.say(f'{attack_emoji}|{source.name} {attack_text} {target.name} используя {self.name}! '
                               f'Нанесено {damage} урона.')
        else:
            source.session.say(f'💨|{source.name} {attack_text} {target.name} используя {self.name}, но не попадает.')
