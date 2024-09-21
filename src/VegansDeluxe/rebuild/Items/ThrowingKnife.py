from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag, percentage_chance
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Enemies
from VegansDeluxe.core import Item
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class ThrowingKnife(Item):
    id = 'throwing_knife'
    name = ls("rebuild.item.throwing_knife.name")


@AttachedAction(ThrowingKnife)
class ThrowingKnifeAction(DecisiveItem):
    id = 'throwing_knife'
    target_type = Enemies()

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.HARMFUL]

    @property
    def name(self):
        return ls("rebuild.item.throwing_knife_name_percentage").format(self.hit_chance)

    @property
    def hit_chance(self):
        return 40 + self.source.energy * 10

    async def func(self, source, target):
        source.energy -= 1
        if not percentage_chance(self.hit_chance):
            self.session.say(ls("rebuild.item.throwing_knife_name_miss").format(source.name, target.name))
            return

        bleeding = target.get_state('bleeding')
        if bleeding.active:
            bleeding.bleeding -= 1
        bleeding.active = True
        self.session.say(
            ls("rebuild.item.throwing_knife.text").format(source.name, target.name)
        )
