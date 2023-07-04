from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import DecisiveWeaponAction
from core.Entities import Entity
from core.Sessions import Session
from core.TargetType import Allies
from core.Weapons.Weapon import Weapon


class WaterGun(Weapon):
    id = 'watergun'
    name = 'Водомет'
    description = 'Дальний бой, урон 1-3. Способность: создаёт водяной щит вокруг цели, из-за чего та не ' \
                  'может загореться три хода, восстанавливает 2 энергии в ход и получает +1 урона.'

    def __init__(self, source):
        super().__init__(source)
        self.cubes = 3
        self.accuracy_bonus = 1
        self.energy_cost = 3
        self.damage_bonus = 0
        self.ranged = True

        self.cooldown_turn = 0


@AttachedAction(WaterGun)
class CreateWaterShield(DecisiveWeaponAction):
    id = 'watershield'
    name = 'Водяной щит'
    target_type = Allies()

    def __init__(self, session: Session, source: Entity, weapon: WaterGun):
        super().__init__(session, source, weapon)
        self.weapon: WaterGun = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.cooldown_turn

    def func(self, source, target):  # TODO: Finish Watergun
        """
            aflame = self.source.get_skill('aflame')
                aflame.extinguished = True
                aflame.flame = 1
                if self.session.event.top == 'attack':
                    damage = self.source.action.data.get('damage')
                    if damage:
                        self.source.action.data.update({'damage': damage + 1})
                if self.session.event.top != 'post-damages':
                    return
                self.source.say(f'🔋|{self.source.name} получает 2 энергии.')
                self.source.energy += 2
                if self.session.turn >= self.turn:
                    self.active = False
                    self.session.say(f'💨|Водяной щит {self.source.name} испарился!')
        """
        self.weapon.cooldown_turn = self.session.turn + 5
        self.session.say(f'💧|{source.name} создаёт водяной щит вокруг {target.name}.')
