from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
import random

from core.TargetType import TargetType, Enemies


class Bow(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 24
        self.cubes = 3
        self.accuracybonus = 1
        self.energycost = 3
        self.dmgbonus = 0
        self.ranged = True

        self.name = 'Лук'
        self.description = 'Дальний бой, урон 1-3, точность средняя. Способность: поджигает стрелу, которая не ' \
                           'наносит урон, но накладывает на цель 2 эффекта горения.'

        self.cooldown_turn = 0
        self.strike = False

    @property
    def actions(self):
        if self.owner.session.turn < self.cooldown_turn:
            return super().actions
        return [
            DecisiveAction(self.fire_arrow, self.owner, target_type=Enemies(),
                           name='Огненная стрела', id='fire_arrow')
        ] + super().actions

    def fire_arrow(self, source, target):
        self.cooldown_turn = source.session.turn + 5
        source.session.say(f'☄️|{source.name} поджигает стрелу и запускает ее в {target.name}!')
        aflame = target.get_skill('aflame')
        if aflame.flame == 0:
            source.session.say(f'🔥|{target.name} загорелся!')
        else:
            source.session.say(f'🔥|Огонь {target.name} усиливается!')
        aflame.flame += 2
        aflame.dealer = self.owner
