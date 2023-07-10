from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Events.EventManager import event_manager
from core.Events.Events import PostTickGameEvent
from core.Weapons.Weapon import Weapon, RangedWeapon
from modern.States.Injury import Injury


class Saw(RangedWeapon):
    id = 'saw'
    name = 'Пиломет'
    description = 'Дальний бой, урон 1-1, точность высокая. имеет шанс наложить на цель эффект "ранен", ' \
                  'увеличивающий урон от атак по цели на 1.'

    def __init__(self):
        super().__init__()
        self.cubes = 2
        self.accuracy_bonus = 3
        self.energy_cost = 3
        self.damage_bonus = 0


@AttachedAction(Saw)
class SawAttack(Attack):
    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        self.session.say(f'{target.name} ранен! ({target.get_skill(Injury.id).injury})')

        @event_manager.now(self.session.id, PostTickGameEvent)
        def func(event: PostTickGameEvent):
            injury = target.get_skill(Injury.id)
            injury.injury += 1

        return damage
