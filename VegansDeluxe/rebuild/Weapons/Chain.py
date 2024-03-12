import random

from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core import AttachedAction, Nearest, RegisterWeapon
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import DeliveryPackageEvent, DeliveryRequestEvent
from VegansDeluxe.core import Enemies, Distance
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon
from VegansDeluxe.rebuild.Weapons.Fist import Fist


@RegisterWeapon
class Chain(MeleeWeapon):
    id = 'chain'
    name = 'Цепь'
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: с шансом выбивает оружие врага из ' \
                  'рук. Если враг перезаряжается, шанс равен 100%.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Chain)
class ChainAttack(MeleeAttack):
    pass


@AttachedAction(Chain)
class KnockWeapon(MeleeAttack):
    id = 'knock_weapon'
    name = 'Выбить оружие'
    priority = -1
    target_type = Enemies(distance=Distance.NEARBY_ONLY)

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        @Nearest(self.session.id, event=DeliveryPackageEvent)
        def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager

            self.weapon.cooldown_turn = self.session.turn + 6
            damage = self.attack(source, target)
            if not damage:
                self.session.say(f'⛓💨|{source.name} не получилось выбить оружие из рук {target.name}!')
                return

            source_reloading = 'reload' not in [a.id for a in
                                                action_manager.get_queued_entity_actions(self.session, target)]
            if source_reloading or random.randint(1, 100) <= 10:
                self.session.say(f'⛓|{source.name} выбил оружие из рук {target.name}!')
                state = target.get_state('knocked-weapon')
                state.weapon = target.weapon
                target.weapon = Fist(self.session.id, target.id)
            else:
                self.session.say(f'⛓💨|{source.name} не получилось выбить оружие из рук {target.name}!')

        self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))
