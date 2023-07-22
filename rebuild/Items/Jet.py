from core.Actions.ActionManager import AttachedAction
from core.Events.EventManager import event_manager
from core.Items.Item import Item
from core.Actions.ItemAction import FreeItem
from core.Events.Events import PostDamagesGameEvent, PreMoveGameEvent
from core.TargetType import Allies


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

        @event_manager.at(self.session.id, turn=self.session.turn + 2, event=PostDamagesGameEvent, priority=3)
        def jet_reload(message: PostDamagesGameEvent):
            self.session.say(f"💉|Энергия {target.name} восстановлена до максимальной! "
                             f"({target.max_energy})")

        @event_manager.at(self.session.id, turn=self.session.turn + 3, event=PreMoveGameEvent, priority=3)
        def jet_reload(message: PreMoveGameEvent):
            target.energy = target.max_energy
