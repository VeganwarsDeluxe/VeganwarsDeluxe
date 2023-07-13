from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import RangedAttack, MeleeAttack
from core.TargetType import Enemies
from core.Weapons.Weapon import RangedWeapon


class Bow(RangedWeapon):
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

        self.cooldown_turn = 0
        self.strike = False


@AttachedAction(Bow)
class BowAttack(MeleeAttack):
    pass


@AttachedAction(Bow)
class FireArrow(RangedAttack):
    id = 'fire_arrow'
    name = 'Огненная стрела'
    target_type = Enemies()

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 5
        damage = self.calculate_damage(source, target)
        source.energy = max(source.energy - self.weapon.energy_cost, 0)
        if not damage:
            self.session.say(f'💨|{source.name} поджигает стрелу и запускает ее в {target.name}, но не попадает.')
            return
        self.session.say(f'☄️|{source.name} поджигает стрелу и запускает ее в {target.name}!')
        aflame = target.get_skill('aflame')
        aflame.add_flame(self.session, target, source, 2)
