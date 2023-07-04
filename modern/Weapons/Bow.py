from core.Actions.Action import DecisiveAction
from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon


class Bow(Weapon):
    id = 'bow'
    name = 'Лук'
    description = 'Дальний бой, урон 1-3, точность средняя. Способность: поджигает стрелу, которая не ' \
                  'наносит урон, но накладывает на цель 2 эффекта горения.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 1
        self.energy_cost = 3
        self.damage_bonus = 0
        self.ranged = True

        self.cooldown_turn = 0
        self.strike = False


@AttachedAction(Bow)
class BowAttack(Attack):
    pass


@AttachedAction(Bow)
class FireArrow(DecisiveAction):
    id = 'fire_arrow'
    name = 'Огненная стрела'

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 5
        damage = self.weapon.calculate_damage(source, target)
        source.energy = max(source.energy - self.weapon.energycost, 0)
        if not damage:
            self.session.say(f'💨|{source.name} поджигает стрелу и запускает ее в {target.name}, но не попадает.')
            return
        self.session.say(f'☄️|{source.name} поджигает стрелу и запускает ее в {target.name}!')
        aflame = target.get_skill('aflame')
        aflame.add_flame(source, 2)
