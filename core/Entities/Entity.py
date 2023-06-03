from core.Action import DecisiveAction, Action
from core.Weapons.Weapon import Weapon
from core.Skills.Skill import Skill
from core.Items.Item import Item
from core.TargetType import TargetType


class Entity:
    def __init__(self, session):
        self.session = session

        self.name: str = ''

        self.hp: int = 0
        self.max_hp: int = 0
        self.dead = False

        self.energy: int = 0
        self.max_energy: int = 0

        self.weapon: Weapon = Weapon(self)
        self.skills: list[Skill] = []
        self.items: list[Item] = []

        self.nearby_entities: list[Entity] = []

        self.team = None

        # Temporary
        self.inbound_dmg: int = 0
        self.outbound_dmg: int = 0
        self.cache = {}

        self.pre_move()
        self.actions: list[Action] = []
        self.using_items: list[Item] = []

        self.action: Action = self.default_actions[0]
        self.target: Entity = self

    def get_action(self, id: str):
        result = list(filter(lambda a: a.id == id, self.actions))
        if result:
            return result[0]

    def get_skill(self, id: str):
        result = list(filter(lambda s: s.id == id, self.skills))
        if result:
            return result[0]

    def get_targets(self, target_type: TargetType = TargetType()):
        if target_type.me:
            return [self]
        # TODO: Fix in necromancy
        targets = filter(lambda t: t != self, self.session.alive_entities)
        if target_type.melee:
            targets = list(filter(lambda t: t in self.nearby_entities, targets))
        if target_type.all:
            return targets
        elif target_type.ally:
            return list(filter(lambda t: self.is_ally(t), targets))
        elif not target_type.ally:
            return list(filter(lambda t: not self.is_ally(t), targets))
        raise RuntimeError(f'{self.action.id} - wrong type')

    def is_ally(self, target):
        if target.team is None or self.team is None:
            return False
        return target.team == self.team

    @property
    def targets(self):
        return self.nearby_entities if not self.weapon.ranged else \
            [entity for entity in self.session.entities if entity != self]

    @property
    def default_actions(self):
        actions = [
            DecisiveAction(self.skip, 'Пропустить', 'skip', type=TargetType(me=True)),
            DecisiveAction(self.reload, 'Перезарядка', 'reload', type=TargetType(me=True)),
        ]
        actions += self.weapon.actions
        for skill in self.skills:
            actions += skill.actions
        if not self.approached:
            actions += [
                DecisiveAction(self.approach, 'Подойти', 'approach', type=TargetType(me=True))
            ]
        return actions

    def say(self, text):
        self.session.say(f'💬|{self.name}: {text}')

    @property
    def approached(self):
        return self.nearby_entities == [entity for entity in self.session.entities if entity != self]

    def pre_move(self):
        self.outbound_dmg = 0
        self.inbound_dmg = 0
        self.cache = {}
        self.actions = self.default_actions
        self.using_items = []

    def tick_turn(self):
        pass

    @property
    def hit_chance(self, *args):
        energy = self.energy + self.weapon.accuracybonus if self.energy else 0
        cubes = self.weapon.cubes
        return int(max((1 - ((1 - energy / 10) ** cubes)) * 100, 0))

    def skip(self, *args):
        self.session.say(f"⬇|{self.name} пропускает ход.")

    def reload(self, *args):
        self.energy = self.max_energy
        self.session.say(f"🕓|{self.name} перезаряжается. Энергия восстановлена до максимальной! ({self.max_energy})")

    def approach(self, *args):
        self.nearby_entities = [entity for entity in self.session.entities if entity != self]
        for entity in self.nearby_entities:
            entity.nearby_entities.append(self) if self not in entity.nearby_entities else None
        self.session.say(f'👣|{self.name} подходит к противнику вплотную.')
