from core.TargetType import TargetType, Enemies
from core.Weapons.Weapon import Weapon
from core.Action import DecisiveAction


class Shest(Weapon):
    id = 45
    name = 'Шест'
    description = 'Ближний бой, урон 1-3. Способность: вы пытаетесь сбить соперника с ног, получая ' \
                  'возможность атаковать даже тех, кто не находится с вами в ближнем бою.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.owner.session.turn < self.cooldown_turn:
            return super().actions
        return super().actions + [
            DecisiveAction(self.knock_down, self.owner,
                           target_type=Enemies(), name='Сбить с ног', id='knock_down')
        ]

    def knock_down(self, source, target):
        self.cooldown_turn = source.session.turn + 6
        damage = self.attack(source, target)
        if not damage:
            source.session.say(f'🚷💨|{source.name} не удалось сбить {target.name} с ног!')
            return
        source.session.say(f'🚷|{source.name} сбивает {target.name} с ног! {target.name} теряет равновесие и падает!')
        state = target.get_skill('knockdown')
        state.active = True
