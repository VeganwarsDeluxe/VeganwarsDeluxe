from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At

from VegansDeluxe.core import Item
from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import PostDamagesGameEvent, PreMoveGameEvent
from VegansDeluxe.core import Allies


@RegisterItem
class Jet(Item):
    id = 'jet'
    name = 'Джет'


@AttachedAction(Jet)
class JetAction(FreeItem):
    id = 'jet'
    name = 'Джет'
    target_type = Allies()

    def func(self, source, target):
        self.session.say(f"💉|{source.name} использует джет на {target.name}! Его энергия будет"
                         f" полностью восстановлена через 2 хода.")

        @At(self.session.id, turn=self.session.turn + 2, event=PostDamagesGameEvent, priority=3)
        def jet_reload(context: EventContext[PostDamagesGameEvent]):
            self.session.say(f"💉|Энергия {target.name} восстановлена до максимальной! "
                             f"({target.max_energy})")

        @At(self.session.id, turn=self.session.turn + 3, event=PreMoveGameEvent, priority=3)
        def jet_reload(context: EventContext[PreMoveGameEvent]):
            target.energy = target.max_energy
