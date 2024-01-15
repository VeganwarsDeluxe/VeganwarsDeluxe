from core.ContentManager import AttachedAction, RegisterItem
from core.Context import EventContext
from core.ContentManager import At

from core.Items.Item import Item
from core.Actions.ItemAction import FreeItem
from core.Events.Events import PostDamagesGameEvent, PreMoveGameEvent
from core.TargetType import Allies


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
