from core.ContentManager import AttachedAction
from core.Actions.WeaponAction import DecisiveWeaponAction, MeleeAttack
from core.Context import EventContext
from core.ContentManager import At
from core.Entities import Entity
from core.Events.DamageEvents import PostAttackGameEvent

from core.Sessions import Session
from core.TargetType import Enemies
from core.Weapons.Weapon import MeleeWeapon


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
