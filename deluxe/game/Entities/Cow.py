from core.Items.Item import FreeItem
from core.TargetType import TargetType, OwnOnly
from .Dummy import Dummy
import modern
from core.Action import DecisiveAction
import random


class Cow(Dummy):
    def __init__(self, session):
        super().__init__(session, name='Корова|🐮')

        self.hp = 1
        self.max_hp = 1
        self.max_energy = 5

        self.team = 'cows'

    def choose_act(self):
        super().choose_act()

        self.action = random.choice([
            EatGrassReload(self), WalkAway(self), Silence(self), Run(self),
            CowApproach(self) if random.choice([True, False]) else Silence(self),
        ])
        self.item_queue.append(Milk(self)) if self.action.id == 'silence' else None


class CowApproach(DecisiveAction):
    id = 'cow_approach'
    name = 'Подойти'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, source.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        source.session.say(f'👣|{source.name} с интересом подходит.')


class Silence(DecisiveAction):
    id = 'cow_silence'
    name = 'Тихо стоять'

    def __init__(self, source):
        super().__init__(source, OwnOnly())


class Run(DecisiveAction):
    id = 'cow_dodge'
    name = 'Перебегать поле'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.session.say(f'💨|{source.name} перебегает поле!')


class WalkAway(DecisiveAction):
    id = 'cow_walk_away'
    name = 'Отойти'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        for entity in source.nearby_entities:
            entity.nearby_entities.remove(source) if source in entity.nearby_entities else None
        source.nearby_entities = []
        source.session.say(f'👣|{source.name} отходит подальше.')


class EatGrassReload(DecisiveAction):
    id = 'reload'
    name = 'Пощипать травку'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.session.say(f'🌿|{source.name} щипает травку. Енергия восстановлена ({source.max_energy})!')
        source.energy = source.max_energy


class Milk(FreeItem):
    id = 'milk'
    name = 'Молоко'

    def __init__(self, source):
        super().__init__(source, target_type=OwnOnly())

    def use(self):
        if self.source.team == 'cows':
            return
        self.target.energy = self.target.max_energy
        self.target.session.say(f'🥛|{self.source.name} пьет молоко! '
                                f'Его енергия восстановлена!')
