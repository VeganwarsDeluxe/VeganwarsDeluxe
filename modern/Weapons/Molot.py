from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
import random

from core.TargetType import TargetType, Enemies


class Molot(Weapon):
    id = 39
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
        return [
            DecisiveAction(self.true_strike, self.owner, target_type=Enemies(distance=1),
                           name='Точный удар', id='true_strike')
        ] + super().actions

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def attack_text(self, source, target, damage):
        if self.strike and damage:
            source.session.say(f'🔨|{source.name} наносит точный удар по {target.name}! Нанесено {damage} урона.')
        else:
            super().attack_text(source, target, damage)

    def true_strike(self, source, target):
        self.cooldown_turn = source.session.turn + 6
        self.owner.energy -= 4
        self.strike = True
        damage = self.attack(source, target)
        self.strike = False
    
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
