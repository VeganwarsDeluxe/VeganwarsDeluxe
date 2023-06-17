from core.Weapons.Weapon import Weapon
from core.Action import FreeAction, ImmediateAction
from core.TargetType import TargetType, OwnOnly


class Claws(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 26
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.name = 'Стальные когти'
        self.description = 'Ближний бой, урон 1-3, точность высокая. Можно выдвинуть когти, повысив урон до 2-5, ' \
                           'но затрачивая 4 энергии за атаку.'

        self.claws = False

    @property
    def actions(self):
        text = 'Выдвинуть когти' if not self.claws else 'Задвинуть когти'
        return super().actions + [
            ImmediateAction(self.switch_claws, self.owner, OwnOnly(), text, 'switch_claws')
        ]

    def switch_claws(self, source, target):
        if not self.claws:
            self.cubes = 4
            self.dmgbonus = 1
            self.energycost = 3
            self.accuracybonus = 1
        else:
            self.cubes = 3
            self.dmgbonus = 0
            self.energycost = 2
        self.claws = not self.claws
        source.session.say(f"⚙️|{source.name} {'выдвигает' if not self.claws else 'задвигает'} когти!")