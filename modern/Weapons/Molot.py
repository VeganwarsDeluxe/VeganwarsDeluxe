from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import DecisiveWeaponAction, MeleeAttack
from core.Entities import Entity
from core.Sessions import Session
from core.TargetType import Enemies, Distance
from core.Weapons.Weapon import MeleeWeapon


class Molot(MeleeWeapon):
    id = 'molot'
    name = 'Молот'
    description = 'Ближний бой, урон 1-3. Способность: за каждые две недостающие единицы энергии ' \
                  'получает +1 к урону.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0

        self.cooldown_turn = 0
        self.strike = False


@AttachedAction(Molot)
class MolotAttack(MeleeAttack):
    priority = -3

    def __init__(self, session: Session, source: Entity, weapon: Molot):
        super().__init__(session, source, weapon)
        self.weapon: Molot = weapon

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def attack_text(self, source, target, damage):
        if self.weapon.strike and damage:
            self.session.say(f'🔨|{source.name} наносит точный удар по {target.name}! Нанесено {damage} урона.')
        else:
            super().attack_text(source, target, damage)

    def calculate_damage(self, source, target):
        if not self.weapon.strike:
            damage = super().calculate_damage(source, target)
        else:
            damage = self.cubes + self.dmgbonus
        if not damage:
            return damage
        return damage + self.energy_bonus(source)


@AttachedAction(Molot)
class TrueStrike(DecisiveWeaponAction):
    id = 'true_strike'
    name = 'Точный удар'
    target_type = Enemies(distance=Distance.NEARBY_ONLY)

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn or self.source.energy < 4

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        source.energy -= 4
        self.weapon.strike = True
        self.attack(source, target)
        self.weapon.strike = False
