import random

from core.Weapons.Weapon import Weapon
from core.States.State import State
from core.Action import DecisiveAction
from core.TargetType import Enemies, Allies, Everyone


class PortalGun(Weapon):  # TODO: Fix or delete
    id = 'portalgun'
    name = 'Портальная пушка'
    description = 'Дальний бой, урон 1-2.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 2
        self.accuracybonus = 1
        self.energycost = 3
        self.dmgbonus = 0
        self.ranged = True

        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return super().actions
        actions = [
            # DecisiveAction(self.retreat, self.owner, target_type=Everyone(),
            #                name='🔵|Создать портал', id='retreat_portal'),
            # DecisiveAction(self.teleport_approach, self.owner, target_type=Everyone(),
            #                name='🟠|Создать портал', id='approach_portal'),
            # DecisiveAction(self.knock_down_portal, self.owner, target_type=Enemies(),
            #                name='🔴|Создать портал', id='knock_down_portal')
        ]
        # return super().actions + [random.choice(actions)]

    def attack_text(self, source, target, damage):
        attack_emoji = "⚡️"
        if damage:
            source.session.say(f'{attack_emoji}|{source.name} стреляет в {target.name} гипер-частицами! '
                               f'Нанесено {damage} урона.')
        else:
            source.session.say(f'🔘|{source.name} направляет пушку на {target.name}, но она не работает.')

    def retreat(self, source, target):
        self.cooldown_turn = source.session.turn + 4
        for entity in target.nearby_entities:
            entity.nearby_entities.remove(target) if target in entity.nearby_entities else None
        target.nearby_entities = []
        target.session.say(f'🔵|{source.name} телепортирует {target.name} подальше от всех!')

    def teleport_approach(self, source, target):
        self.cooldown_turn = source.session.turn + 4
        target.nearby_entities = list(filter(lambda t: t != target, target.session.entities))
        for entity in target.nearby_entities:
            entity.nearby_entities.append(target) if target not in entity.nearby_entities else None
        target.session.say(f'🟠|{source.name} телепортирует {target.name} в центр!')

    def knock_down_portal(self, source, target):
        self.cooldown_turn = source.session.turn + 4
        source.session.say(f'🔴|{source.name} создает портал под ногами у {target.name}! {target.name} падает!')
        state = target.get_skill('knockdown')
        state.active = True

    def attack(self, source, target):
        return super().attack(source, target)
