from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, RangedAttack
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import After
from VegansDeluxe.core import Entity
from VegansDeluxe.core import AttackGameEvent

from VegansDeluxe.core import PreDamagesGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import Allies
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class WaterGun(RangedWeapon):
    id = 'watergun'
    name = 'Водомет'
    description = 'Дальний бой, урон 1-3. Способность: создаёт водяной щит вокруг цели, из-за чего та не ' \
                  'может загореться три хода, восстанавливает 2 энергии в ход и получает +1 урона.'

    cubes = 3
    accuracy_bonus = 1
    energy_cost = 3
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(WaterGun)
class PistolAttack(RangedAttack):
    pass


@AttachedAction(WaterGun)
class CreateWaterShield(DecisiveWeaponAction):
    id = 'watershield'
    name = 'Водяной щит'
    target_type = Allies()

    def __init__(self, session: Session, source: Entity, weapon: WaterGun):
        super().__init__(session, source, weapon)
        self.weapon: WaterGun = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.cooldown_turn

    def func(self, source, target):
        @After(self.session.id, 0, event=PreDamagesGameEvent, repeats=3)
        def _(context: EventContext[PreDamagesGameEvent]):
            aflame = self.source.get_state('aflame')
            aflame.extinguished = True
            aflame.flame = 0

            self.session.say(f'🔋|{self.source.name} получает 2 энергии.')
            self.source.energy += 2
            if self.session.turn >= self.turn:
                self.active = False
                self.session.say(f'💨|Водяной щит {self.source.name} испарился!')

        @After(self.session.id, 0, event=AttackGameEvent, repeats=3)
        def _(context: EventContext[AttackGameEvent]):
            if context.event.source != self.source:
                return
            if context.event.damage:
                context.event.damage += 1

        self.weapon.cooldown_turn = self.session.turn + 5
        self.session.say(f'💧|{source.name} создаёт водяной щит вокруг {target.name}.')
