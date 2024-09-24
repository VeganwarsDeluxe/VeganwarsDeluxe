import random

from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Enemies
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Item
from VegansDeluxe.core import Session
from VegansDeluxe.core.Translator.LocalizedList import LocalizedList
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild import Aflame


@RegisterItem
class Molotov(Item):
    id = 'molotov'
    name = ls("rebuild.item.molotov.name")


@AttachedAction(Molotov)
class MolotovAction(DecisiveItem):
    id = 'molotov'
    name = ls("rebuild.item.molotov.name")
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source, item)
        self.tags += [ActionTag.HARMFUL]

        self.range = 2

    async def func(self, source: Entity, target: Entity):
        targets = []
        for _ in range(self.range):
            target_pool = list(filter(lambda t: t not in targets,
                                      self.get_targets(source, Enemies())
                                      ))
            if not target_pool:
                continue
            target = random.choice(target_pool)
            target: Entity

            aflame = target.get_state(Aflame)
            aflame.add_flame(self.session, target, source, 1)
            targets.append(target)
        source.energy = max(source.energy - 2, 0)
        self.session.say(
            ls("rebuild.item.molotov.text").format(source.name, LocalizedList([t.name for t in targets]))
        )

    @property
    def blocked(self):
        return self.source.energy < 2

