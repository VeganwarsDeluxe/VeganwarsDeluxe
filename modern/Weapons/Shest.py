from core.Actions.Action import DecisiveAction
from core.TargetType import Enemies
from core.Weapons.Weapon import Weapon


class Shest(Weapon):
    id = 'shest'
    name = 'Шест'
    description = 'Ближний бой, урон 1-3. Способность: вы пытаетесь сбить соперника с ног, получая ' \
                  'возможность атаковать даже тех, кто не находится с вами в ближнем бою.'

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
        return super().actions + [
            KnockDown(self.source, self)
        ]


class KnockDown(DecisiveAction):
    id = 'knock_down'
    name = 'Сбить с ног'

    def __init__(self, source, weapon):
        super().__init__(source, Enemies())
        self.weapon = weapon

    def func(self, source, target):
        self.weapon.cooldown_turn = source.session.turn + 6
        damage = self.weapon.attack(source, target)
        if not damage:
            source.session.say(f'🚷💨|{source.name} не удалось сбить {target.name} с ног!')
            return
        source.session.say(f'🚷|{source.name} сбивает {target.name} с ног! {target.name} теряет равновесие и падает!')
        state = target.get_skill('knockdown')
        state.active = True
