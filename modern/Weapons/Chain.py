from core.Actions.Action import DecisiveAction
from core.Actions.ActionManager import action_manager, AttachedAction
from core.Actions.WeaponAction import Attack, DecisiveWeaponAction
from core.TargetType import Enemies, Distance
from core.Weapons.Weapon import Weapon, MeleeWeapon
from modern.Weapons.Fist import Fist


class Chain(MeleeWeapon):
    id = 'chain'
    name = 'Цепь'
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: с шансом выбивает оружие врага из ' \
                  'рук. Если враг перезаряжается, шанс равен 100%.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0
        self.cooldown_turn = 0


@AttachedAction(Chain)
class ChainAttack(Attack):
    pass


@AttachedAction(Chain)
class KnockWeapon(DecisiveWeaponAction):
    id = 'knock_weapon'
    name = 'Выбить оружие'
    priority = -1
    target_type = Enemies(distance=Distance.ANY)

    def hidden(self) -> bool:
        return self.session.turn < self.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 3
        self.weapon.attack(source, target)
        if target.action.id != 'reload':
            self.session.say(f'⛓💨|{source.name} не получилось выбить оружие из рук {target.name}!')
        else:
            self.session.say(f'⛓|{source.name} выбил оружие из рук {target.name}!')
            state = target.get_skill('knocked-weapon')
            state.weapon = target.weapon
            target.weapon = Fist()
