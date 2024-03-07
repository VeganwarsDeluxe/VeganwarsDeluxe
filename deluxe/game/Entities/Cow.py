import random

from VegansDeluxe.core.Actions.Action import DecisiveAction
from VegansDeluxe.core import AttachedAction
from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import Item
from VegansDeluxe.core import OwnOnly
from deluxe.startup import engine
from .Dummy import Dummy


class Cow(Dummy):
    def __init__(self, session_id: str):
        super().__init__(session_id, name='Корова|🐮')

        self.hp = 3
        self.max_hp = 1
        self.max_energy = 5

        self.team = 'cows'

    def choose_act(self, session):
        super().choose_act(session)

        while True:
            action = engine.action_manager.get_action(session, self, random.choice(["cow_approach", "cow_silence", "cow_dodge",
                                                                             "cow_walk_away", "reload"]))
            if not action:
                continue
            if not action.targets:
                continue
            action.target = random.choice(action.targets)
            engine.action_manager.queue_action(session, self, action.id)
            break


@AttachedAction(Cow)
class CowApproach(DecisiveAction):
    id = 'cow_approach'
    name = 'Подойти'
    target_type = OwnOnly()

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, self.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        self.session.say(f'👣|{source.name} с интересом подходит.')


@AttachedAction(Cow)
class Silence(DecisiveAction):
    id = 'cow_silence'
    name = 'Тихо стоять'
    target_type = OwnOnly()

    def func(self, source, target):
        source.items.append(MilkItem())


@AttachedAction(Cow)
class Run(DecisiveAction):
    id = 'cow_dodge'
    name = 'Перебегать поле'
    target_type = OwnOnly()

    def func(self, source, target):
        self.source.inbound_accuracy_bonus = -5
        self.session.say(f'💨|{source.name} перебегает поле!')


@AttachedAction(Cow)
class WalkAway(DecisiveAction):
    id = 'cow_walk_away'
    name = 'Отойти'
    target_type = OwnOnly()

    def func(self, source, target):
        for entity in source.nearby_entities:
            entity.nearby_entities.remove(source) if source in entity.nearby_entities else None
        source.nearby_entities = []
        self.session.say(f'👣|{source.name} отходит подальше.')


@AttachedAction(Cow)
class EatGrassReload(DecisiveAction):
    id = 'eat_grass'
    name = 'Пощипать травку'
    target_type = OwnOnly()

    def func(self, source, target):
        self.session.say(f'🌿|{source.name} щипает травку. Енергия восстановлена ({source.max_energy})!')
        source.energy = source.max_energy


class MilkItem(Item):
    id = 'milk'
    name = 'Молоко'


@AttachedAction(MilkItem)
class Milk(FreeItem):
    id = 'milk'
    name = 'Молоко'
    target_type = OwnOnly()

    def use(self):
        if self.source.team == 'cows':
            return
        self.target.energy = self.target.max_energy
        self.session.say(f'🥛|{self.source.name} пьет молоко! '
                         f'Его енергия восстановлена!')
