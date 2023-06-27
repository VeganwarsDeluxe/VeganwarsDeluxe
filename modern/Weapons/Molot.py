from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
import random

from core.TargetType import TargetType, Enemies


class Molot(Weapon):
    id = 'molot'
    name = 'Молот'
    description = 'Ближний бой, урон 1-3. Способность: за каждые две недостающие единицы энергии ' \
                  'получает +1 к урону.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.cooldown_turn = 0
        self.strike = False

    @property
    def actions(self):
        if self.owner.session.turn < self.cooldown_turn or self.owner.energy < 4:
            return super().actions
        return [TrueStrike(self.owner, self)] + super().actions

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def attack_text(self, source, target, damage):
        if self.strike and damage:
            source.session.say(f'🔨|{source.name} наносит точный удар по {target.name}! Нанесено {damage} урона.')
        else:
            super().attack_text(source, target, damage)
    
    def calculate_damage(self, source, target):
        if not self.strike:
            damage = super().calculate_damage(source, target)
        else:
            damage = self.cubes + self.dmgbonus
        if not damage:
            return damage
        return damage + self.energy_bonus(source)

    def attack(self, source, target):
        return super().attack(source, target)


class TrueStrike(DecisiveAction):
    id = 'true_strike'
    name = 'Точный удар'

    def __init__(self, source, weapon):
        super().__init__(source, Enemies(distance=1))
        self.weapon = weapon

    def func(self, source, target):
        self.weapon.cooldown_turn = source.session.turn + 6
        self.weapon.owner.energy -= 4
        self.weapon.strike = True
        self.weapon.attack(source, target)
        self.weapon.strike = False
