from core.TargetType import TargetType
from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
from modern.Weapons.Fist import Fist


class Chain(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 16
        self.name = 'Цепь'
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.owner.session.turn < self.cooldown_turn:
            return super().actions
        return super().actions + [
            DecisiveAction(self.knock_weapon, 'Выбить оружие',
                           'knock_weapon', type=TargetType(ally=False, melee=True))
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


