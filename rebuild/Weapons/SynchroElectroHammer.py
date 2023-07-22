import random

from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.WeaponAction import DecisiveWeaponAction, MeleeAttack
from core.Entities import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import PreMoveGameEvent
from core.Sessions import Session
from core.TargetType import Enemies, Distance, OwnOnly
from core.Weapons.Weapon import MeleeWeapon


class SynchroElectroHammer(MeleeWeapon):
    id = 'synchro_electro_hammer'
    name = 'Синхроэлектромолот'
    description = 'Ближний бой.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = -1
        self.damage_bonus = 0

        self.cooldown_turn = 0
        self.strike = False


@AttachedAction(SynchroElectroHammer)
class MolotAttack(MeleeAttack):
    priority = -3

    def __init__(self, session: Session, source: Entity, weapon: SynchroElectroHammer):
        super().__init__(session, source, weapon)
        self.weapon: SynchroElectroHammer = weapon

    def energy_bonus(self, source):
        return (source.max_energy - source.energy) // 2

    def send_attack_message(self, source, target, damage):
        if self.weapon.strike and damage:
            self.session.say(f'🔨|{source.name} наносит точный удар по {target.name}! Нанесено {damage} урона.')
        else:
            super().send_attack_message(source, target, damage)


@AttachedAction(SynchroElectroHammer)
class SyncHammer(DecisiveWeaponAction):
    id = 'synchronize_hammer'
    name = 'Синхронизировать'
    target_type = OwnOnly()
    priority = 0

    def func(self, source, target):
        source.energy = 9999
        source.max_energy = 9999
        source.hp = 9999
        source.max_hp = 9999

        @event_manager.nearest(self.session.id, PreMoveGameEvent)
        def a(e):
            for i in range(1000):
                action_manager.queue_action(self.session, source, "rage-serum")

        self.session.say(f'🌐{source} синхронизируется с {self.session}. Начинается '
                         f'{random.choice(event_manager._handlers)}.')
