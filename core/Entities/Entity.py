from core.Action import DecisiveAction, Action
from core.Weapons.Weapon import Weapon
from core.Skills.Skill import Skill
from core.Items.Item import Item
from core.TargetType import OwnOnly
from core.DamageHolder import DamageHolder


class Entity:
    def __init__(self, session, name=''):
        self.session = session

        self.name: str = name

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
        self.inbound_dmg = DamageHolder()
        self.outbound_dmg = DamageHolder()
        self.cache = {}

        self.pre_move()
        self.actions: list[Action] = []

        self.action_queue: list[Action] = []
        self.item_queue: list[Item] = []

        self.action: Action = self.default_actions[0]
        self.target: Entity = self

    @property
    def hearts(self):
        return '♥️' * self.hp if self.hp < 8 else f"♥️x{self.hp}"

    @property
    def energies(self):
        return '⚡️' * self.energy if self.energy < 8 else f"⚡️x{self.energy}"

    def get_action(self, id: str, default=False):
        pool = self.actions
        if default:
            pool = self.default_actions
        action = list(filter(lambda a: a.id == id, pool))
        if action:
            action = action[0]
            action.source = self
            return action

    def get_item(self, id: str):
        items = list(filter(lambda i: i.id == id, self.items))
        if items:
            item = items[0]
            item.source = self
            return item

    def remove_action(self, id: str):
        action = self.get_action(id)
        if not action:
            return
        self.actions.remove(action)

    def get_skill(self, id: str):
        result = list(filter(lambda s: s.id == id, self.skills))
        if result:
            return result[0]

    def is_ally(self, target):
        if target == self:
            return True
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
            DecisiveAction(self.skip, self, target_type=OwnOnly(), name='Пропустить', id='skip'),
            DecisiveAction(self.reload, self, target_type=OwnOnly(), name='Перезарядка', id='reload'),
        ]
        actions += self.weapon.actions
        for skill in self.skills:
            actions += skill.actions
        if not self.approached:
            actions += [
                DecisiveAction(self.approach, self, target_type=OwnOnly(), name='Подойти', id='approach')
            ]
        return actions

    def say(self, text):
        self.session.say(f'💬|{self.name}: {text}')

    @property
    def approached(self):
        return self.nearby_entities == list(filter(lambda t: t != self, self.session.entities))

    def update_actions(self):
        self.actions = self.default_actions

    def pre_move(self):
        self.outbound_dmg.clear()
        self.inbound_dmg.clear()
        self.cache = {}
        self.item_queue = []
        self.action_queue = []

    def tick_turn(self):
        pass

    @property
    def hit_chance(self, *args):
        if self.energy <= 0:
            return 0
        energy = self.energy + self.weapon.accuracybonus if self.energy else 0
        cubes = self.weapon.cubes
        return int(max((1 - ((1 - energy / 10) ** cubes)) * 100, 0))

    def skip(self, *args):
        self.session.say(f"⬇|{self.name} пропускает ход.")

    def reload(self, *args):
        self.energy = self.max_energy
        self.session.say(f"🕓|{self.name} перезаряжается. Энергия восстановлена до максимальной! ({self.max_energy})")

    def approach(self, *args):
        self.nearby_entities = list(filter(lambda t: t != self, self.session.entities))
        for entity in self.nearby_entities:
            entity.nearby_entities.append(self) if self not in entity.nearby_entities else None
        self.session.say(f'👣|{self.name} подходит к противнику вплотную.')
