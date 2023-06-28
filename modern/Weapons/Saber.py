from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction
from core.TargetType import Enemies


class Saber(Weapon):
    id = 'saber'
    name = 'Сабля'
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: можно выбрать любого врага. ' \
                  'Если тот атаковал, урон от его атаки полностью блокируется, а энергия цели снижается до 0.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return super().actions
        return [
            Parry(self.source, self)
        ] + super().actions

    def attack(self, source, target):
        return super().attack(source, target)


class Parry(DecisiveAction):
    id = 'Парировать'
    name = 'parry'

    def __init__(self, source, weapon):
        super().__init__(source, Enemies(), priority=-5)
        self.weapon = weapon

    def func(self, source, target):
        self.weapon.cooldown_turn = source.session.turn + 5
        source.session.say(f'🗡|{source.name} готовится парировать.')

        @source.session.handlers.at(turn=source.session.turn, events='post-attack')
        def parry():
            if target.action.id != 'attack':
                return
            attack_target = target.action.data.get('target')
            if not attack_target:
                return
            if attack_target != source:
                return
            damage = target.action.data.get('damage')
            if not damage:
                return

            source.session.say(f'🗡|{source.name} парирует атаку {target.name}! Урон заблокирован,'
                               f' {target.name} теряет всю энергию!')
            target.energy = 0
            target.action.data.update({'damage': 0})
