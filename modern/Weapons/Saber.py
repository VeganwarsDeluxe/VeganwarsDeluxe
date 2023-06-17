from core.Weapons.Weapon import Weapon
from core.States.State import State
from core.Action import DecisiveAction
from core.TargetType import Enemies


class Saber(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 22
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.name = 'Сабля'
        self.description = 'Ближний бой, урон 1-3, точность высокая. Способность: можно выбрать любого врага. ' \
                           'Если тот атаковал, урон от его атаки полностью блокируется, а энергия цели снижается до 0.'

        self.cooldown_turn = 0
        self.state = Parrying(self.owner)
        self.owner.skills.append(self.state)

    @property
    def actions(self):
        if self.owner.session.turn < self.cooldown_turn:
            return super().actions
        return [
            DecisiveAction(self.parry, self.owner, target_type=Enemies(distance=1),
                           name='Парировать', id='parry', priority=-5)
        ] + super().actions

    def parry(self, source, target):
        self.cooldown_turn = source.session.turn + 5
        self.state.dealer = target
        source.session.say(f'🗡|{source.name} готовится парировать.')

    def attack(self, source, target):
        return super().attack(source, target)


class Parrying(State):
    def __init__(self, source):
        super().__init__(source, id='parrying', name='Парирование', constant=True)
        self.dealer = None

    def __call__(self):
        source = self.source
        if source.session.current_stage != 'post-attack':
            return
        if not self.dealer:
            return
        if self.dealer.action.id != 'attack':
            return
        target = self.dealer.action.data.get('target')
        if not target:
            return
        if target != self.source:
            return
        damage = self.dealer.action.data.get('damage')
        if not damage:
            return

        source.session.say(f'🗡|{source.name} парирует атаку {self.dealer.name}! Урон заблокирован,'
                           f' {self.dealer.name} теряет всю энергию!')
        self.dealer.energy = 0
        self.dealer.action.data.update({'damage': 0})

        self.dealer = None
