from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, MeleeAttack
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostAttackGameEvent

from VegansDeluxe.core import Session
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Saber(MeleeWeapon):
    id = 'saber'
    name = 'Сабля'
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: можно выбрать любого врага. ' \
                  'Если тот атаковал, урон от его атаки полностью блокируется, а энергия цели снижается до 0.'

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
    name = 'Парировать'
    id = 'parry'
    priority = -4
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Saber):
        super().__init__(session, source, weapon)
        self.weapon: Saber = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 5
        self.session.say(f'🗡|{source.name} готовится парировать.')

        @At(self.session.id, turn=self.session.turn, event=PostAttackGameEvent)
        def parry(context: EventContext[PostAttackGameEvent]):
            if target != context.event.source:
                return
            if context.event.target != source:
                return
            if not context.event.damage:
                return

            self.session.say(f'🗡|{source.name} парирует атаку {target.name}! Урон заблокирован,'
                             f' {target.name} теряет всю энергию!')
            target.energy = 0
            context.event.damage = 0
