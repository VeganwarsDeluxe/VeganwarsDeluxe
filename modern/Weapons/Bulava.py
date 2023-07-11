from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Entities import Entity
from core.Sessions import Session
from core.Weapons.Weapon import Weapon, MeleeWeapon


class Bulava(MeleeWeapon):
    id = 'bulava'
    name = 'Булава'
    description = 'Ближний бой, урон 1-3, точность высокая. За каждую атаку подряд по одной и той же цели ' \
                  'вы получаете +1 урона.'

    def __init__(self):
        super().__init__(cubes=3, accuracy_bonus=2, energy_cost=2, damage_bonus=0)
        self.consecutive_target = None, 0
        self.last_attack_turn = 0


@AttachedAction(Bulava)
class BulavaAttack(Attack):
    def __init__(self, session: Session, source: Entity, weapon: Bulava):
        super().__init__(session, source, weapon)
        self.weapon: Bulava = weapon

    def calculate_damage(self, source: Entity, target: Entity) -> int:
        """
        Calculates the damage dealt to the target, with bonus damage for consecutive attacks on the same target.
        """
        damage = super().calculate_damage(source, target)
        if not damage:
            return damage
        consecutive_target, bonus = self.weapon.consecutive_target
        if consecutive_target == target:
            damage += bonus
        return damage

    def attack(self, source: Entity, target: Entity) -> int:
        """
        Attacks the target and keeps track of consecutive attacks on the same target for damage bonus.
        """
        damage = super().attack(source, target)
        consecutive_target, bonus = self.weapon.consecutive_target
        if consecutive_target == target and self.weapon.last_attack_turn == self.session.turn - 1:
            self.weapon.consecutive_target = target, bonus + 1
        else:
            self.weapon.consecutive_target = target, 1
        self.weapon.last_attack_turn = self.session.turn
        return damage
