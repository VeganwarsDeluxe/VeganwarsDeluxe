from .Weapon import Weapon
from core.Action import FreeAction


class Claws(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 26
        self.name = 'Стальные когти'
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.claws = False

    @property
    def actions(self):
        return super().actions + [
            FreeAction(self.switch_claws, 'Сменить статус когтей', 'switch_claws')
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
        source.say(f'I {"enable" if self.claws else "disable"} my claws!')