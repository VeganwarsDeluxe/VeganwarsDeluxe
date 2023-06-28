from core.TargetType import TargetType, Enemies
from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
from modern.Weapons.Fist import Fist


class Chain(Weapon):
    id = 'chain'
    name = 'Цепь'
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: с шансом выбивает оружие врага из ' \
                  'рук. Если враг перезаряжается, шанс равен 100%.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0
        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return super().actions
        return super().actions + [
            KnockWeapon(self.source, self)
        ]


class KnockWeapon(DecisiveAction):
    id = 'knock_weapon'
    name = 'Выбить оружие'

    def __init__(self, source, weapon):
        super().__init__(source, Enemies(distance=1))
        self.weapon = weapon

    def func(self, source, target):
        self.weapon.cooldown_turn = source.session.turn + 3
        self.weapon.attack(source, target)
        if target.action.id != 'reload':
            source.session.say(f'⛓💨|{source.name} не получилось выбить оружие из рук {target.name}!')
        else:
            source.session.say(f'⛓|{source.name} выбил оружие из рук {target.name}!')
            state = target.get_skill('knocked-weapon')
            state.weapon = target.weapon
            target.weapon = Fist(target)
