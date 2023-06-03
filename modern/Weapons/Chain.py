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
            DecisiveAction(self.knock_weapon, 'Вьібить оружие',
                           'knock_weapon', type=TargetType(ally=False, melee=False))
        ]

    def knock_weapon(self, source, target):
        self.cooldown_turn = source.session.turn + 3
        if target.action.id != 'reload':
            source.say(f'Я попьітался вьібить оружие {target.name}, но у меня не получилось!')
        else:
            source.say(f'Я вьібил оружие {target.name}!')
            target.weapon = Fist(target)


