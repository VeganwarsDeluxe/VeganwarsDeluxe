from core.Action import DecisiveAction, Action
from core.Weapons.Weapon import Weapon
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
        self.skills = []
        self.items: list[Item] = []

        self.nearby_entities: list[Entity] = []

        self.team = None

        # Temporary
        self.inbound_dmg = DamageHolder()
        self.outbound_dmg = DamageHolder()

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

    def get_action(self, action_id: str, default=False):
        pool = self.actions
        if default:
            pool = self.default_actions
        action = list(filter(lambda a: a.id == action_id, pool))
        if action:
            action = action[0]
            action.source = self
            return action

    def get_item(self, item_id: str):
        items = list(filter(lambda i: i.id == item_id, self.items))
        if items:
            item = items[0]
            item.source = self
            return item

    def remove_action(self, item_id: str):
        action = self.get_action(item_id)
        if not action:
            return
        self.actions.remove(action)

    def get_skill(self, item_id: str):
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
    def default_actions(self):
        actions = [
            SkipTurnAction(self),
            ReloadAction(self)
        ]
        actions += self.weapon.actions
        for skill in self.skills:
            actions += skill.actions
        if not self.approached:
            actions += [
                ApproachAction(self)
            ]
        return actions

    def say(self, text):
        self.session.say(f'💬|{self.name}: {text}')

    @property
    def approached(self):
        return self.nearby_entities == list(filter(lambda t: t != self, self.session.entities))

    @property
    def targets(self):
        return self.nearby_entities if not self.weapon.ranged else \
            [entity for entity in self.session.entities if entity != self]

    def update_actions(self):
        self.actions = self.default_actions

    def pre_move(self):
        self.outbound_dmg.clear()
        self.inbound_dmg.clear()
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


class ApproachAction(DecisiveAction):
    id = 'approach'
    name = 'Подойти'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, source.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        source.session.say(f'👣|{source.name} подходит к противнику вплотную.')


class ReloadAction(DecisiveAction):
    id = 'reload'
    name = 'Перезарядка'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.energy = source.max_energy
        source.session.say(f"🕓|{source.name} перезаряжается. "
                           f"Энергия восстановлена до максимальной! ({source.max_energy})")


class SkipTurnAction(DecisiveAction):
    id = 'skip'
    name = 'Пропустить'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.session.say(f"⬇|{source.name} пропускает ход.")
