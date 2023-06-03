from core.Action import FreeAction, DecisiveAction, Action
from core.Weapons.Weapon import Weapon
from core.Skills.Skill import Skill


class Entity:
    def __init__(self, session):
        self.session = session

        self.name: str = ''

        self.hp: int = 0
        self.max_hp: int = 0
        self.dead = False

        self.energy: int = 0
        self.max_energy: int = 0

        self.weapon: Weapon = Weapon()
        self.skills: list[Skill] = []

        self.nearby_entities: list[Entity] = []

        # Temporary
        self.inbound_dmg: int = 0
        self.outbound_dmg: int = 0

        self.action: Action = self.actions[0]
        self.target: Entity = self

    @property
    def targets(self):
        return self.nearby_entities if not self.weapon.ranged else \
            [entity for entity in self.session.entities if entity != self]

    @property
    def actions(self):
        actions = [
            DecisiveAction(self.skip, 'Пропустить', 'skip'),
            DecisiveAction(self.reload, 'Перезарядка', 'reload'),
        ]
        actions += self.weapon.actions
        for skill in self.skills:
            actions += skill.actions
        if not self.approached:
            actions += [
                DecisiveAction(self.approach, 'Подойти', 'approach')
            ]
        return actions

    def say(self, text):
        print(f'[{self.name}] {text}')

    @property
    def approached(self):
        return self.nearby_entities == [entity for entity in self.session.entities if entity != self]

    def tick_turn(self):
        self.outbound_dmg = 0
        self.inbound_dmg = 0

    @property
    def hit_chance(self, *args):
        energy = self.energy + self.weapon.accuracybonus if self.energy else 0
        cubes = self.weapon.cubes
        return (1 - ((1 - energy / 10) ** cubes)) * 100

    def skip(self, *args):
        self.say("Skipping turn.")

    def reload(self, *args):
        self.energy = self.max_energy
        self.say("Reloaded.")

    def approach(self, *args):
        self.nearby_entities = [entity for entity in self.session.entities if entity != self]
        for entity in self.nearby_entities:
            entity.nearby_entities.append(self) if self not in entity.nearby_entities else None
        self.say('Approaching!')
