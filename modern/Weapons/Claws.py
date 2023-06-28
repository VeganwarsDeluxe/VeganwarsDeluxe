from core.Weapons.Weapon import Weapon
from core.Action import FreeAction, ImmediateAction
from core.TargetType import TargetType, OwnOnly


class Claws(Weapon):
    id = 'claws'
    name = 'Стальные когти'
    description = 'Ближний бой, урон 1-3, точность высокая. Можно выдвинуть когти, повысив урон до 2-5, ' \
                  'но затрачивая 4 энергии за атаку.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.claws = False

    @property
    def actions(self):
        return super().actions + [
            SwitchClaws(self.source, self)
        ]


class SwitchClaws(ImmediateAction):
    id = 'switch_claws'

    @property
    def name(self):
        return 'Выдвинуть когти' if not self.weapon.claws else 'Задвинуть когти'

    def __init__(self, source, weapon):
        super().__init__(source, OwnOnly())
        self.weapon = weapon

    def func(self, source, target):
        if not self.weapon.claws:
            self.weapon.cubes = 4
            self.weapon.dmgbonus = 1
            self.weapon.energycost = 3
            self.weapon.accuracybonus = 1
        else:
            self.weapon.cubes = 3
            self.weapon.dmgbonus = 0
            self.weapon.energycost = 2
        self.weapon.claws = not self.weapon.claws
        source.session.say(f"⚙️|{source.name} {'выдвигает' if not self.weapon.claws else 'задвигает'} когти!")
