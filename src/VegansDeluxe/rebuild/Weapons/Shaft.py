from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import Enemies
from VegansDeluxe.core import Entity
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core import Session
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon
from VegansDeluxe.rebuild.States.KnockDown import Knockdown


@RegisterWeapon
class Shaft(MeleeWeapon):
    id = 'shaft'
    name = ls("rebuild.weapon.shaft.name")
    description = ls("rebuild.weapon.shaft.description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Shaft)
class ShaftAttack(MeleeAttack):
    pass


@AttachedAction(Shaft)
class KnockDown(MeleeAttack):
    id = 'knock_down'
    name = ls("rebuild.weapon.shaft.action.name")
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Shaft):
        super().__init__(session, source, weapon)
        self.weapon: Shaft = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    async def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        damage = (await self.attack(source, target)).dealt
        if not damage:
            self.session.say(ls("rebuild.weapon.shaft.action_miss").format(source.name, target.name))
            return
        self.session.say(ls("rebuild.weapon.shaft.action.text").format(source.name, target.name))
        state = target.get_state(Knockdown)
        state.active = True
