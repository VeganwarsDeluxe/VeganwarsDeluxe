from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Entities import Entity
from core.Sessions import Session
from core.Weapons.Weapon import Weapon


class Bulava(Weapon):
    id = 'bulava'
    name = 'Булава'
    description = 'Ближний бой, урон 1-3, точность высокая. За каждую атаку подряд по одной и той же цели ' \
                  'вы получаете +1 урона.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0

        self.main_target = None, 0
        self.last_attack_turn = 0


@AttachedAction(Bulava)
class BulavaAttack(Attack):
    def __init__(self, session: Session, source: Entity, weapon: Bulava):
        super().__init__(session, source, weapon)
        self.weapon: Bulava = weapon

    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if not damage:
            return damage
        main_target, bonus = self.weapon.main_target
        if main_target == target:
            damage += bonus
        return damage

    def attack(self, source, target):
        damage = super().attack(source, target)
        main_target, bonus = self.weapon.main_target
        if main_target == target and self.weapon.last_attack_turn == self.session.turn - 1:
            self.weapon.main_target = target, bonus + 1
        else:
            self.weapon.main_target = target, 1
        self.weapon.last_attack_turn = self.session.turn
        return damage
