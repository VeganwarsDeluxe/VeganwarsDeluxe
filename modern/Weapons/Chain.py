from core.TargetType import TargetType, Enemies
from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
from modern.Weapons.Fist import Fist


class Chain(Weapon):
    id = 16
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: с шансом выбивает оружие врага из ' \
                  'рук. Если враг перезаряжается, шанс равен 100%.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.name = 'Цепь'
        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.owner.session.turn < self.cooldown_turn:
            return super().actions
        return super().actions + [
            DecisiveAction(self.knock_weapon, self.owner, target_type=Enemies(distance=1),
                           name='Выбить оружие', id='knock_weapon')
        ]

    def knock_weapon(self, source, target):
        self.cooldown_turn = source.session.turn + 3
        self.attack(source, target)
        if target.action.id != 'reload':
            source.session.say(f'⛓💨|{source.name} не получилось выбить оружие из рук {target.name}!')
        else:
            source.session.say(f'⛓|{source.name} выбил оружие из рук {target.name}!')
            state = target.get_skill('knocked-weapon')
            state.weapon = target.weapon
            target.weapon = Fist(target)


