import random

import modern
from core.Actions.Action import DecisiveAction
from core.Actions.ActionManager import action_manager, AttachedAction
from core.Actions.ItemAction import FreeItem
from core.Items.Item import Item
from core.TargetType import OwnOnly
from .Dummy import Dummy


class Elemental(Dummy):
    def __init__(self, session_id: str):
        super().__init__(session_id, name='Веган Елементаль|🌪')

        self.hp = 7
        self.max_hp = 7
        self.energy = 7
        self.max_energy = 7

        self.items = [item() for item in modern.all_items]

        self.team = 'elemental'

    def choose_act(self, session):
        super().choose_act(session)
        self.weapon = random.choice(modern.all_weapons)()
        action_manager.update_entity_actions(session, self)

        cost = False
        while not cost:
            action = random.choice(action_manager.get_available_actions(session, self))
            if self.energy <= 0:
                action_manager.get_action(session, self, "reload")
            else:
                action.target = random.choice(action.targets)
            action_manager.queue_action(session, self, action.id)
            cost = action.cost


@AttachedAction(Elemental)
class WarpReality(DecisiveAction):
    id = 'warp_reality'
    name = 'Искривить пространство'
    target_type = OwnOnly()

    def func(self, source, target):
        self.source.inbound_accuracy_bonus = -5
        self.session.say(f'🌌|{source.name} искривляет пространство.')


@AttachedAction(Elemental)
class Singularity(DecisiveAction):
    id = 'reload'
    name = 'Перезагрузить сингулярность'
    target_type = OwnOnly()

    def func(self, source, target):
        self.session.say(f'⚫️|{source.name} перезагружает сингулярность. Енергия восстановлена ({source.max_energy})!')
        source.energy = source.max_energy
