from core.State import State
from core.Action import DecisiveAction


class KnockedWeapon(State):
    def __init__(self):
        super().__init__(id='knocked-weapon', name='Выбивание оружия', constant=True)
        self.weapon = None

    def __call__(self, source):
        pass

    @property
    def active(self):
        return self.weapon

    def pick_up(self, source, target):
        source.weapon = self.weapon
        source.say(f'Я поднял с пола {self.weapon.name}!')
        self.weapon = None

    @property
    def actions(self):
        if not self.active:
            return []
        return [
            DecisiveAction(self.pick_up, name='Подобрать оружие', id='pick_up')
        ]


