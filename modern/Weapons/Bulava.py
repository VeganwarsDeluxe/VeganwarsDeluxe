from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
import random

from core.TargetType import TargetType


class Bulava(Weapon):
    id = 13
    name = 'Булава'
    description = 'Ближний бой, урон 1-3, точность высокая. За каждую атаку подряд по одной и той же цели ' \
                  'вы получаете +1 урона.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.main_target = None, 0
        self.last_attack_turn = 0
        
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if not damage:
            return damage
        main_target, bonus = self.main_target
        if main_target == target:
            damage += bonus
        return damage

    def attack(self, source, target):
        damage = super().attack(source, target)
        main_target, bonus = self.main_target
        if main_target == target and self.last_attack_turn == source.session.turn-1:
            self.main_target = target, bonus+1
        else:
            self.main_target = target, 1
        self.last_attack_turn = source.session.turn
        return damage
