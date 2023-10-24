from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import DecisiveWeaponAction, RangedAttack
from core.Context import Context
from core.Decorators import RegisterEvent
from core.Entities import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import PreMoveGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.TargetType import Enemies
from core.Weapons.Weapon import RangedWeapon


class Rifle(RangedWeapon):
    id = 'sniperRifle'
    name = 'Снайперская винтовка'
    description = 'Дальний бой, урон 8-8, точность очень низкая. Можно прицелиться вместо атаки,' \
                  ' чтобы повысить точность против выбранного персонажа'

    cubes = 1
    accuracy_bonus = -4
    energy_cost = 5
    damage_bonus = 7

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.main_target = None, 0

        session = session_manager.get_session(session_id)
        entity = session.get_entity(entity_id)

        @RegisterEvent(session_id=session_id, event=PreMoveGameEvent)
        def pre_move(context: Context[PreMoveGameEvent]):
            main_target, level = self.main_target
            if main_target:
                main_target: Entity

                chance = self.hit_chance(entity)
                if level == 1:
                    chance += 60
                elif level == 2:
                    chance += 90

                entity.notifications += f'🎯|Вероятность попасть по {main_target.name} - {chance}%'


@AttachedAction(Rifle)
class RifleAttack(RangedAttack):
    def __init__(self, session: Session, source: Entity, weapon: Rifle):
        super().__init__(session, source, weapon)
        self.weapon: Rifle = weapon

    def calculate_damage(self, source, target):
        main_target, level = self.weapon.main_target
        if main_target == target:
            self.weapon.accuracy_bonus = 2 if level == 1 else 5
        else:
            self.weapon.accuracy_bonus = -4
        return super().calculate_damage(source, target)

    def func(self, source, target):
        damage = super().attack(source, target)
        self.weapon.main_target = None, 0
        return damage


@AttachedAction(Rifle)
class AimRifle(DecisiveWeaponAction):
    id = 'aim_rifle'
    name = 'Выцелить'
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Rifle):
        super().__init__(session, source, weapon)
        self.weapon: Rifle = weapon

    def func(self, source, target):
        main_target, level = self.weapon.main_target
        self.weapon.main_target = target, min(2, level + 1)
        self.session.say(f'🎯|{source.name} целится.')
