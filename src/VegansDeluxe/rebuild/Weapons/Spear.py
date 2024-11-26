from VegansDeluxe.core import At, OwnOnly
from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, MeleeAttack
from VegansDeluxe.core import Entity
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import PostAttackGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Spear(MeleeWeapon):
    id = 'spear'
    name = ls("rebuild.weapon.spear.name")
    description = ls("rebuild.weapon.spear.description")

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0

    def counter_attack_mode(self, status: bool):
        if status:
            self.energy_cost = 1
            self.damage_bonus = 1
        else:
            self.energy_cost = 2
            self.damage_bonus = 0


@AttachedAction(Spear)
class SpearAttack(MeleeAttack):
    pass


@AttachedAction(Spear)
class CounterAttack(DecisiveWeaponAction):
    name = ls("rebuild.weapon.spear.action.name")
    id = 'counter-attack'
    priority = -4
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, weapon: Spear):
        super().__init__(session, source, weapon)
        self.weapon: Spear = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    async def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 3
        self.session.say(ls("rebuild.weapon.spear.action.text").format(source.name))

        @At(self.session.id, turn=self.session.turn, event=PostAttackGameEvent)
        async def counter_attack(context: EventContext[PostAttackGameEvent]):
            if context.event.target != source:
                return

            self.weapon.counter_attack_mode(True)
            counterattack_action = SpearAttack(self.session, self.source, self.weapon)
            counterattack_action.target = context.event.source
            await counterattack_action.execute()

