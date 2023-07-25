import random

from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.WeaponAction import DecisiveWeaponAction, MeleeAttack
from core.TargetType import Enemies, Distance
from core.Weapons.Weapon import MeleeWeapon
from rebuild.Weapons.Fist import Fist


class Chain(MeleeWeapon):
    id = 'chain'
    name = 'Цепь'
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: с шансом выбивает оружие врага из ' \
                  'рук. Если враг перезаряжается, шанс равен 100%.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@AttachedAction(Chain)
class ChainAttack(MeleeAttack):
    pass


@AttachedAction(Chain)
class KnockWeapon(MeleeAttack):
    id = 'knock_weapon'
    name = 'Выбить оружие'
    priority = -1
    target_type = Enemies(distance=Distance.ANY)

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 3
        self.attack(source, target)
        source_reloading = 'reload' not in [a.id for a in
                                            action_manager.get_queued_entity_actions(self.session, target)]
        if source_reloading or random.randint(1, 100) <= 10:
            self.session.say(f'⛓|{source.name} выбил оружие из рук {target.name}!')
            state = target.get_skill('knocked-weapon')
            state.weapon = target.weapon
            target.weapon = Fist()
        else:
            self.session.say(f'⛓💨|{source.name} не получилось выбить оружие из рук {target.name}!')
