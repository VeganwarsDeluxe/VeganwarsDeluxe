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
            DecisiveAction(self.eat_grass, self, OwnOnly(), 'reload'),
            DecisiveAction(self.walk_away, self, OwnOnly(), 'walk_away'),
            DecisiveAction(self.silence, self, OwnOnly(), 'silence'),
            DecisiveAction(self.run, self, OwnOnly(), 'dodge'),
            DecisiveAction(self.approach, self, OwnOnly(), 'approach') if random.choice([True, False])
            else DecisiveAction(self.silence, self, OwnOnly(), 'silence'),
        ])

    def run(self, source, target):
        source.session.say(f'💨|{source.name} перебегает поле!')

    def eat_grass(self, source, target):
        source.session.say(f'🌿|{source.name} щипает травку. Енергия восстановлена ({self.max_energy})!')
        self.energy = self.max_energy

    def approach(self, *args):
        self.nearby_entities = list(filter(lambda t: t != self, self.session.entities))
        for entity in self.nearby_entities:
            entity.nearby_entities.append(self) if self not in entity.nearby_entities else None
        self.session.say(f'👣|{self.name} с интересом подходит.')

    def walk_away(self, *args):
        for entity in self.nearby_entities:
            entity.nearby_entities.remove(self) if self in entity.nearby_entities else None
        self.nearby_entities = []
        self.session.say(f'👣|{self.name} отходит подальше.')
