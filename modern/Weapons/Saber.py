from core.Events.Events import PostAttackGameEvent
from core.Weapons.Weapon import Weapon
from core.Actions.Action import DecisiveAction
from core.TargetType import Enemies


class Saber(Weapon):
    id = 'saber'
    name = 'Сабля'
    description = 'Ближний бой, урон 1-3, точность высокая. Способность: можно выбрать любого врага. ' \
                  'Если тот атаковал, урон от его атаки полностью блокируется, а энергия цели снижается до 0.'

    def __init__(self, source):
        super().__init__(source)
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

        @source.session.event_manager.now(source.session.id, event=PostAttackGameEvent)
        def parry(event: PostAttackGameEvent):
            if target != event.source:
                return
            if event.target != source:
                return
            if not event.damage:
                return

            source.session.say(f'🗡|{source.name} парирует атаку {target.name}! Урон заблокирован,'
                               f' {target.name} теряет всю энергию!')
            event.target.energy = 0
            event.damage = 0
