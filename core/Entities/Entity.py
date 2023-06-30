from core.Weapons.Weapon import Weapon
from core.Items.Item import Item
from core.DamageHolder import DamageHolder


class Entity:
    def __init__(self, session_id, name=''):
        self.session_id = session_id
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

    @property
    def hearts(self):
        return '♥️' * self.hp if self.hp < 8 else f"♥️x{self.hp}"

    @property
    def energies(self):
        return '⚡️' * self.energy if self.energy < 8 else f"⚡️x{self.energy}"

    def get_item(self, item_id: str):
        items = list(filter(lambda i: i.id == item_id, self.items))
        if items:
            item = items[0]
            item.source = self
            return item

    def get_skill(self, skill_id: str):
        result = list(filter(lambda s: s.id == skill_id, self.skills))
        if result:
            return result[0]

    def is_ally(self, target):
        if target == self:
            return True
        if target.team is None or self.team is None:
            return False
        return target.team == self.team

    def pre_move(self):
        self.outbound_dmg.clear()
        self.inbound_dmg.clear()

    def tick_turn(self):
        pass

    """
    @property
    def hit_chance(self, *args):
        if self.energy <= 0:
            return 0
        energy = self.energy + self.weapon.accuracybonus if self.energy else 0
        cubes = self.weapon.cubes
        return int(max((1 - ((1 - energy / 10) ** cubes)) * 100, 0))
    """
