from core.Actions.Action import DecisiveAction
from core.TargetType import Enemies
from core.Weapons.Weapon import Weapon


class Bow(Weapon):
    id = 'bow'
    name = 'Лук'
    description = 'Дальний бой, урон 1-3, точность средняя. Способность: поджигает стрелу, которая не ' \
                  'наносит урон, но накладывает на цель 2 эффекта горения.'

    def __init__(self, source):
        super().__init__(source)
        self.cubes = 3
        self.accuracybonus = 1
        self.energycost = 3
        self.dmgbonus = 0
        self.ranged = True

        self.cooldown_turn = 0
        self.strike = False

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return super().actions
        return [FireArrow(self.source, self)] + super().actions


class FireArrow(DecisiveAction):
    id = 'fire_arrow'
    name = 'Огненная стрела'

    def __init__(self, source, weapon):
        super().__init__(source, Enemies())
        self.weapon = weapon

    def func(self, source, target):
        self.weapon.cooldown_turn = source.session.turn + 5
        damage = self.weapon.calculate_damage(source, target)
        source.energy = max(source.energy - self.weapon.energycost, 0)
        if not damage:
            source.session.say(f'💨|{source.name} поджигает стрелу и запускает ее в {target.name}, но не попадает.')
            return
        source.session.say(f'☄️|{source.name} поджигает стрелу и запускает ее в {target.name}!')
        aflame = target.get_skill('aflame')
        aflame.add_flame(source, 2)
