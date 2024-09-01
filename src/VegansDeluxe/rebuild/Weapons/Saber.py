from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, MeleeAttack
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostAttackGameEvent

from VegansDeluxe.core import Session
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Saber(MeleeWeapon):
    id = 'saber'
    name = ls("weapon_saber_name")
    description = ls("weapon_saber_description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Saber)
class FistAttack(MeleeAttack):
    pass


@AttachedAction(Saber)
class Parry(DecisiveWeaponAction):
    name = ls("weapon_saber_action_name")
    id = 'parry'
    priority = -4
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Saber):
        super().__init__(session, source, weapon)
        self.weapon: Saber = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    async def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 5
        self.session.say(ls("weapon_saber_action_text").format(source.name))

        @At(self.session.id, turn=self.session.turn, event=PostAttackGameEvent)
        def parry(context: EventContext[PostAttackGameEvent]):
            if target != context.event.source:
                return
            if context.event.target != source:
                return
            if not context.event.damage:
                return

            self.session.say(ls("weapon_saber_action_effect").format(source.name, target.name))
            target.energy = 0
            context.event.damage = 0
