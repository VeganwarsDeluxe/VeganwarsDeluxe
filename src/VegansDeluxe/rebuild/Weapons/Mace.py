from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Session
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Mace(MeleeWeapon):
    id = 'mace'
    name = ls("weapon_mace_name")
    description = ls("weapon_mace_description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.consecutive_target = None, 0
        self.last_attack_turn = 0


@AttachedAction(Mace)
class MaceAttack(MeleeAttack):
    def __init__(self, session: Session, source: Entity, weapon: Mace):
        super().__init__(session, source, weapon)
        self.weapon: Mace = weapon

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

    def func(self, source: Entity, target: Entity) -> int:
        """
        Attacks the target and keeps track of consecutive attacks on the same target for damage bonus.
        """
        consecutive_target, bonus = self.weapon.consecutive_target
        if consecutive_target == target and self.weapon.last_attack_turn == self.session.turn - 1:
            self.weapon.consecutive_target = target, bonus + 1
        else:
            self.weapon.consecutive_target = target, 1
        self.weapon.last_attack_turn = self.session.turn
        damage = super().attack(source, target).dealt
        return damage
