from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import Enemies, Distance
from VegansDeluxe.core import Entity
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core import Session
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Molot(MeleeWeapon):
    id = 'molot'
    name = ls("rebuild.weapon.molot.name")
    description = ls("rebuild.weapon.molot.description")

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

    def calculate_damage(self, source, target, *args):
        if not self.weapon.strike:
            damage = super().calculate_damage(source, target, *args)
        else:
            damage = self.weapon.cubes + self.weapon.damage_bonus
        if not damage:
            return damage
        return damage + self.energy_bonus(source)


@AttachedAction(Molot)
class TrueStrike(MeleeAttack):
    id = 'true_strike'
    name = ls("rebuild.weapon.molot.action.name")
    target_type = Enemies(distance=Distance.NEARBY_ONLY)
    priority = -3

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn or self.source.energy < 4

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def calculate_damage(self, source, target, *args):
        damage = self.weapon.cubes + self.weapon.damage_bonus
        if not super().calculate_damage(source, target, *args):
            return damage
        return damage + self.energy_bonus(source)

    async def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        source.energy -= 4
        await self.attack(source, target, pay_energy=False)
