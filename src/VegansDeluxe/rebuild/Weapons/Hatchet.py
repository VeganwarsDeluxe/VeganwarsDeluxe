from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import Entity
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core import Session
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Hatchet(MeleeWeapon):
    id = 'hatchet'
    name = ls("rebuild.weapon.hatchet.name")
    description = ls("rebuild.weapon.hatchet.description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.hatchet_bonus = 4


@AttachedAction(Hatchet)
class HatchetAttack(MeleeAttack):
    def __init__(self, session: Session, source: Entity, weapon: Hatchet):
        super().__init__(session, source, weapon)
        self.weapon: Hatchet = weapon

    def calculate_damage(self, *args):
        damage = super().calculate_damage(*args)
        if not damage:
            return
        return damage + self.weapon.hatchet_bonus

    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        if damage:
            self.weapon.hatchet_bonus = max(self.weapon.hatchet_bonus - 1, 0)
        return damage
