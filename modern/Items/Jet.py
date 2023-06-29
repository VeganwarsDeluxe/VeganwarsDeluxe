from core.Items.Item import FreeItem
from core.Events.Events import PostDamagesGameEvent
from core.TargetType import Allies


class Jet(FreeItem):
    id = 'jet'
    name = 'Джет'

    def __init__(self, source):
        super().__init__(source, target_type=Allies())

    def use(self):
        self.source.session.say(f"💉|{self.source.name} использует джет на {self.target.name}! Его энергия будет"
                                f" полностью восстановлена через 2 хода.")

        @self.source.session.event_manager.at(self.source.session.id, turn=self.source.session.turn + 2,
                                              event=PostDamagesGameEvent)
        def jet_reload(message: PostDamagesGameEvent):
            self.target.energy = self.target.max_energy
            self.source.session.say(f"💉|Энергия {self.target.name} восстановлена до максимальной! "
                                    f"({self.target.max_energy})")
