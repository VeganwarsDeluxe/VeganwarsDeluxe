from VegansDeluxe.core import State, Skill, Weapon, Item, Entity
from VegansDeluxe.matchmakery.Matches.Match import Match


class ModManager:
    def __init__(self):
        self.__mods = []

class Mod:
    def __init__(self):
        self.id: str
        self.version: str
        self.requires: list[str]

        # Path to the "localizations" folder.
        self.localizations: str

        self.entities: list[type[Entity]]
        self.weapons: list[type[Weapon]]
        self.states: list[type[State]]
        self.skills: list[type[Skill]]
        self.items: list[type[Item]]

        self.matches: list[type[Match]]

        # If you want a mod with REALLY extra stuff and your implementation supports that - so be it.
        self.extra: dict


mod_manager = ModManager()
