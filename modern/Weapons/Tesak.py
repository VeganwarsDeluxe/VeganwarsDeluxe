from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Entities import Entity
from core.Sessions import Session
from core.Weapons.Weapon import Weapon


class Tesak(Weapon):
    id = 'tesak'
    name = "Тесак"
    description = 'Ближний бой, урон 1-3. Имеет изначальный бонус урона 3, за каждое попадание ' \
                  'по цели бонус уменьшается на 1.'

    def __init__(self, source):
        super().__init__(source)
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0
        self.ranged = False

        self.tesak_bonus = 4


@AttachedAction(Tesak)
class RifleAttack(Attack):
    def __init__(self, session: Session, source: Entity, weapon: Tesak):
        super().__init__(session, source, weapon)
        self.weapon: Tesak = weapon

    def calculate_damage(self, source, target):
        return super().calculate_damage(source, target) + self.tesak_bonus

    def attack(self, source, target):
        damage = super().attack(source, target)
        if damage:
            self.weapon.tesak_bonus = max(self.tesak_bonus - 1, 0)
        return damage
