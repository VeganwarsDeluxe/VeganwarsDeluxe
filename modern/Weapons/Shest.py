from core.Actions.Action import DecisiveAction
from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import DecisiveWeaponAction
from core.Entities import Entity
from core.Sessions import Session
from core.TargetType import Enemies
from core.Weapons.Weapon import Weapon


class Shest(Weapon):
    id = 'shest'
    name = 'Шест'
    description = 'Ближний бой, урон 1-3. Способность: вы пытаетесь сбить соперника с ног, получая ' \
                  'возможность атаковать даже тех, кто не находится с вами в ближнем бою.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0

        self.cooldown_turn = 0


@AttachedAction(Shest)
class KnockDown(DecisiveWeaponAction):
    id = 'knock_down'
    name = 'Сбить с ног'
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Shest):
        super().__init__(session, source, weapon)
        self.weapon: Shest = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        damage = self.attack(source, target)
        if not damage:
            self.session.say(f'🚷💨|{source.name} не удалось сбить {target.name} с ног!')
            return
        self.session.say(f'🚷|{source.name} сбивает {target.name} с ног! {target.name} теряет равновесие и падает!')
        state = target.get_skill('knockdown')
        state.active = True
