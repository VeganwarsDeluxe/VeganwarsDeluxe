from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import Enemies, Distance
from VegansDeluxe.core import Entity
from VegansDeluxe.core import MeleeAttack, ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Sledgehammer(MeleeWeapon):
    id = 'sledgehammer'
    name = ls("rebuild.weapon.sledgehammer.name")
    description = ls("rebuild.weapon.sledgehammer.description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Sledgehammer)
class SledgehammerAttack(MeleeAttack):
    pass


@AttachedAction(Sledgehammer)
class SledgehammerCrush(MeleeAttack):
    id = 'crush'
    name = ls("rebuild.weapon.sledgehammer.action.name")
    target_type = Enemies(distance=Distance.NEARBY_ONLY)

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn or self.source.energy < 4

    def calculate_damage(self, source: Entity, target: Entity, *args) -> int:
        if not super().calculate_damage(source, target, *args):
            return 0
        return 1 + target.max_energy - target.energy

    async def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        source.energy -= 4
        await self.attack(source, target, pay_energy=False)
