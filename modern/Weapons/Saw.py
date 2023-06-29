from core.Events.Events import PostTickGameEvent
from core.Weapons.Weapon import Weapon
from modern.States.Injury import Injury


class Saw(Weapon):
    id = 'saw'
    name = 'Пиломет'
    description = 'Дальний бой, урон 1-1, точность высокая. имеет шанс наложить на цель эффект "ранен", ' \
                  'увеличивающий урон от атак по цели на 1.'

    def __init__(self, source):
        super().__init__(source)
        self.cubes = 2
        self.accuracybonus = 3
        self.energycost = 3
        self.dmgbonus = 0
        self.ranged = True

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        source.session.say(f'{target.name} ранен! ({target.get_skill(Injury.id).injury})')

        @source.session.event_manager.now(source.session.id, PostTickGameEvent)
        def func(message: PostTickGameEvent):
            injury = target.get_skill(Injury.id)
            injury.injury += 1

        return damage
