from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import MeleeAttack
from core.Entities import Entity
from core.Sessions import Session
from core.Weapons.Weapon import MeleeWeapon


class Hatchet(MeleeWeapon):
    id = 'hatchet'
    name = "Тесак"
    description = 'Ближний бой, урон 1-3. Имеет изначальный бонус урона 3, за каждое попадание ' \
                  'по цели бонус уменьшается на 1.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self):
        super().__init__()
        self.hatchet_bonus = 4


@AttachedAction(Hatchet)
class HatchetAttack(MeleeAttack):
    def __init__(self, session: Session, source: Entity, weapon: Hatchet):
        super().__init__(session, source, weapon)
        self.weapon: Hatchet = weapon

    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if not damage:
            return
        return damage + self.weapon.hatchet_bonus

    def func(self, source, target):
        damage = super().attack(source, target)
        if damage:
            self.weapon.hatchet_bonus = max(self.weapon.hatchet_bonus - 1, 0)
        return damage
