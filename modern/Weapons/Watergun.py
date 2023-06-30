from core.Actions.Action import DecisiveAction
from core.States.State import State
from core.TargetType import Allies
from core.Weapons.Weapon import Weapon


class Saber(Weapon):
    id = 'watergun'
    name = 'Водомет'
    description = 'Дальний бой, урон 1-3. Способность: создаёт водяной щит вокруг цели, из-за чего та не ' \
                  'может загореться три хода, восстанавливает 2 энергии в ход и получает +1 урона.'

    def __init__(self, source):
        super().__init__(source)
        self.cubes = 3
        self.accuracybonus = 1
        self.energycost = 3
        self.dmgbonus = 0
        self.ranged = True

        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return super().actions
        return [
            CreateWaterShield(self.source, self)
        ] + super().actions

    def attack(self, source, target):
        return super().attack(source, target)


class CreateWaterShield(DecisiveAction):
    id = 'watershield'
    name = 'Водяной щит'

    def __init__(self, source, weapon):
        super().__init__(source, Allies())
        self.weapon = weapon

    def func(self, source, target):
        state = target.get_skill('watershield')
        if not state:
            state = WaterShield(target)
            target.skills.append(state)

        self.weapon.cooldown_turn = source.session.turn + 5
        state.turn = source.session.turn + 3
        state.active = True
        source.session.say(f'💧|{source.name} создаёт водяной щит вокруг {target.name}.')


class WaterShield(State):
    id = 'watershield'
    name = 'Водяной щит'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.active = False
        self.turn = 0

    def __call__(self):
        if not self.active:
            return
        aflame = self.source.get_skill('aflame')
        aflame.extinguished = True
        aflame.flame = 1
        if self.source.session.event.top == 'attack':
            damage = self.source.action.data.get('damage')
            if damage:
                self.source.action.data.update({'damage': damage + 1})
        if self.source.session.event.top != 'post-damages':
            return
        self.source.say(f'🔋|{self.source.name} получает 2 энергии.')
        self.source.energy += 2
        if self.source.session.turn >= self.turn:
            self.active = False
            self.source.session.say(f'💨|Водяной щит {self.source.name} испарился!')
        pass
