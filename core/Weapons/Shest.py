from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction


class Shest(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 45
        self.name = 'Шест'
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
            DecisiveAction(self.knock_down, 'Сбить с ног', 'knock_down', type='enemy')
        ]

    def knock_down(self, source, target):
        self.cooldown_turn = source.session.turn + 3
        source.say(f'Я сбил {target.name} с ног!')
