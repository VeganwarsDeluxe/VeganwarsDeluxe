from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import RangedAttack
from core.Context import EventContext
from core.Decorators import Nearest
from core.Events.EventManager import event_manager
from core.Events.Events import PostTickGameEvent
from core.Weapons.Weapon import RangedWeapon
from rebuild.States.Injury import Injury


class Saw(RangedWeapon):
    id = 'saw'
    name = 'Пиломет'
    description = 'Дальний бой, урон 1-1, точность высокая. имеет шанс наложить на цель эффект "ранен", ' \
                  'увеличивающий урон от атак по цели на 1.'

    cubes = 2
    accuracy_bonus = 3
    energy_cost = 3
    damage_bonus = 0


@AttachedAction(Saw)
class SawAttack(RangedAttack):
    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        self.session.say(f'{target.name} ранен! ({target.get_skill(Injury.id).injury})')

        @Nearest(self.session.id, PostTickGameEvent)
        def func(context: EventContext[PostTickGameEvent]):
            injury = target.get_skill(Injury.id)
            injury.injury += 1

        return damage
