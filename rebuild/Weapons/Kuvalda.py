from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import DecisiveWeaponAction, MeleeAttack
from core.Entities import Entity
from core.Sessions import Session
from core.TargetType import Enemies, Distance
from core.Weapons.Weapon import MeleeWeapon


class Kuvalda(MeleeWeapon):
    id = 'kuvalda'
    name = 'Кувалда'
    description = 'Ближний бой, урон 1-3. Способность: Вы можете сокрушить цель, ' \
                  'нанося ей (1 + потраченная энергия цели) урона и затрачивая 4 энергии.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Kuvalda)
class KuvaldaAttack(MeleeAttack):
    pass


@AttachedAction(Kuvalda)
class KuvaldaCrush(MeleeAttack):
    id = 'crush'
    name = 'Сокрушить'
    target_type = Enemies(distance=Distance.NEARBY_ONLY)

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn or self.source.energy < 4

    def calculate_damage(self, source: Entity, target: Entity) -> int:
        if not super().calculate_damage(source, target):
            return 0
        return 1 + target.max_energy - target.energy

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        source.energy -= 4
        self.attack(source, target, pay_energy=False)
