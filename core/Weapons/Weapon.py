import random
from core.Action import DecisiveAction
from core.TargetType import Enemies


class Weapon:
    id = 'None'
    name = 'None'
    description = 'Описание еще не написано.'

    def __init__(self, owner):
        self.owner = owner
        self.energycost = 2
        self.cubes = 2
        self.dmgbonus = 0
        self.ranged = False
        self.accuracybonus = 0

    @property
    def actions(self):
        return [
            Attack(self.owner, self)
        ]

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
        return damage

    def attack(self, source, target):
        """
        Actually performs attack on target, dealing damage.
        """
        damage = self.calculate_damage(source, target)
        source.energy = max(source.energy - self.energycost, 0)

        source.action.data.update({'damage': damage, 'source': source, 'target': target})
        source.session.stage('attack')                                   # 7.1 Pre-Attack stage
        damage = source.action.data.get('damage')

        self.attack_text(source, target, damage)

        source.action.data.update({'damage': damage, 'source': source, 'target': target})
        source.session.stage('post-attack')  # 7.2 Post-Attack stage
        damage = source.action.data.get('damage')

        target.inbound_dmg.add(source, damage)
        source.outbound_dmg.add(target, damage)
        return damage

    def attack_text(self, source, target, damage):
        attack_text = 'стреляет в' if self.ranged else 'бьет'
        attack_emoji = '💥' if self.ranged else '👊'
        if damage:
            source.session.say(f'{attack_emoji}|{source.name} {attack_text} {target.name} используя {self.name}! '
                               f'Нанесено {damage} урона.')
        else:
            source.session.say(f'💨|{source.name} {attack_text} {target.name} используя {self.name}, но не попадает.')


class Attack(DecisiveAction):
    id = 'attack'
    name = 'Атака'

    def __init__(self, source, weapon, priority=0):
        super().__init__(source, Enemies(distance=not weapon.ranged), priority=priority)
        self.weapon = weapon

    def func(self, source, target):
        self.weapon.attack(source, target)
