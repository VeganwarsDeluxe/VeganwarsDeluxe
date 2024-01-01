from core.Actions.WeaponAction import MeleeAttack
from core.ContentManager import AttachedAction
from core.Entities import Entity
from core.Sessions import Session
from core.TargetType import Enemies, Distance
from core.Weapons.Weapon import MeleeWeapon


class Molot(MeleeWeapon):
    id = 'molot'
    name = 'Молот'
    description = 'Ближний бой, урон 1-3. Способность: за каждые две недостающие единицы энергии ' \
                  'получает +1 к урону.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0
        self.strike = False


@AttachedAction(Molot)
class MolotAttack(MeleeAttack):
    def __init__(self, session: Session, source: Entity, weapon: Molot):
        super().__init__(session, source, weapon)
        self.weapon: Molot = weapon

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def calculate_damage(self, source, target):
        if not self.weapon.strike:
            damage = super().calculate_damage(source, target)
        else:
            damage = self.cubes + self.dmgbonus
        if not damage:
            return damage
        return damage + self.energy_bonus(source)


@AttachedAction(Molot)
class TrueStrike(MeleeAttack):
    id = 'true_strike'
    name = 'Точный удар'
    target_type = Enemies(distance=Distance.NEARBY_ONLY)
    priority = -3

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn or self.source.energy < 4

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def calculate_damage(self, source, target):
        damage = self.weapon.cubes + self.weapon.damage_bonus
        if not super().calculate_damage(source, target):
            return damage
        return damage + self.energy_bonus(source)

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        source.energy -= 4
        self.attack(source, target, pay_energy=False)
