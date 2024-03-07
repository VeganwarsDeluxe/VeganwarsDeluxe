import random

from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import Item
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Enemies


@RegisterItem
class ThrowingKnife(Item):
    id = 'throwing_knife'
    name = 'Метательный нож'


@AttachedAction(ThrowingKnife)
class ThrowingKnifeAction(DecisiveItem):
    id = 'throwing_knife'
    target_type = Enemies()

    @property
    def name(self):
        return f'Метательный нож ({self.hit_chance}%)'

    @property
    def hit_chance(self):
        return 40 + self.source.energy * 10

    def func(self, source, target):
        source.energy -= 1
        if random.randint(0, 100) > self.hit_chance:
            self.session.say(f"💨|{source.name} кидает метательный нож в {target.name}, но не попадает.")
            return
        bleeding = target.get_state('bleeding')
        if bleeding.active:
            bleeding.bleeding -= 1
        bleeding.active = True
        self.session.say(f'🔪|{source.name} кидает метательный нож в {target.name}.\n'
                         f'❣️|{target.name} истекает кровью!')
