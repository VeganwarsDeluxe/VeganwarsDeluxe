from uuid import uuid4

from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Events.EventManager import EventManager
from VegansDeluxe.core.Events.Events import AttachStateEvent
from VegansDeluxe.core.States import State
from VegansDeluxe.core.Translator.LocalizedString import LocalizedString
from VegansDeluxe.core.Weapons.Weapon import Weapon
from VegansDeluxe.core.Items.Item import Item
from VegansDeluxe.core.DamageHolder import DamageHolder


class Entity:
    """
    Entity class. Main actor in the Session - Entities perform Actions.
    """
    type = 'entity'

    def __init__(self,
                 session_id: str = '', name: str = '',
                 hp: int = 0, max_hp: int = 0,
                 energy: int = 0, max_energy: int = 0):

        self.session_id = session_id
        """ID of the Session, that entity belongs to."""

        self.name: str | LocalizedString = name
        """Displayed name of the entity."""

        self.id = str(uuid4())
        """ID of the entity."""

        self.hp: int = hp
        """Current HP of the entity."""
        self.max_hp: int = max_hp
        """Max HP value of the entity."""

        self.dead: bool = False
        """Shows if entity is dead or alive."""

        self.energy: int = energy
        """Current energy of the entity."""
        self.max_energy: int = max_energy
        """Max energy value of the entity."""

        self.weapon: Weapon = Weapon(session_id, self.id)
        """Weapon of the entity."""
        self.states: list[State] = []
        """Entity's list of state and skill instances."""
        self.items: list[Item] = []
        """Entity's list of item instances."""

        self.nearby_entities: list[Entity] = []
        """List of entities that are "nearby" this entity. Influences some Actions."""

        self.team = None
        """Entity's team ID. If None - it fights against everyone."""

        # Temporary
        self.inbound_dmg: DamageHolder = DamageHolder()
        """Temporary variable. Holds info about inbound damage during this turn."""
        self.outbound_dmg = DamageHolder()
        """Temporary variable. Holds info about outbound damage during this turn."""

        self.outbound_accuracy_bonus = 0
        """Temporary variable. Influences accuracy of this entity on this turn."""
        self.inbound_accuracy_bonus = 0
        """Temporary variable. Influences accuracy of other entities targeting this entity this turn."""

        self.notifications: list[str | LocalizedString] = []
        """Temporary variable. List of strings that should be privately displayed to the Entity."""

    @property
    def hit_chance(self) -> int:
        """Returns hit chance of the entity's weapon."""
        if self.weapon:
            return self.weapon.hit_chance(self)
        else:
            return 0

    def map_items_quantity(self) -> dict[str, int]:
        """Maps entity's items to their quantity."""
        item_map = {}
        for item in self.items:
            if item.id not in item_map:
                item_map[item.id] = 0
            item_map[item.id] += 1
        return item_map

    @property
    def hearts(self) -> str:
        """HP emoji display."""
        return '♥️' * self.hp if 0 < self.hp < 8 else f"♥️x{self.hp}"

    @property
    def energies(self) -> str:
        """Energy emoji display."""
        return '⚡️' * self.energy if 0 < self.energy < 8 else f"⚡️x{self.energy}"

    @property
    def skills(self) -> list[Skill]:
        """Returns list of entity's Skills only."""
        return list(filter(lambda s: s.type == 'skill', self.states))

    def get_item(self, item_id: str) -> Item:
        """Returns Item by its ID."""
        items = list(filter(lambda i: i.id == item_id, self.items))
        if items:
            item = items[0]
            item.source = self
            return item

    async def attach_state(self, state: State, event_manager: EventManager):
        self.states.append(state)
        await event_manager.publish(AttachStateEvent(self.session_id, self.id, state))

    def get_state(self, skill_id: str) -> State:
        result = list(filter(lambda s: s.id == skill_id, self.states))
        if result:
            return result[0]

    def is_ally(self, target) -> bool:
        """Tells if a target is in the same team as the entity."""
        if target == self:
            return True
        if target.team is None or self.team is None:
            return False
        return target.team == self.team

    def pre_move(self):
        """
        Clears out temporary variables.

        :todo: Invent attributes like in minecraft or something. Having special variables for this is unwanted.
        """
        self.outbound_dmg.clear()
        self.inbound_dmg.clear()

        self.outbound_accuracy_bonus = 0
        self.inbound_accuracy_bonus = 0

        self.notifications = []

    def tick_turn(self):
        pass
