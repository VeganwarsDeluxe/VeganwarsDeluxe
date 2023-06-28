from core.Items.Item import DecisiveItem, FreeItem
from core.TargetType import Allies, Everyone


class Jet(FreeItem):
    id = 'jet'
    name = 'Джет'

    def __init__(self, source):
        super().__init__(source, target_type=Allies())

    def use(self):
        self.source.session.say(f"💉|{self.source.name} использует джет на {self.target.name}! Его энергия будет"
                                f" полностью восстановлена через 2 хода.")

        @self.source.session.event_manager.at(turn=self.source.session.turn + 2, events='post-damages')
        def jet_reload():
            self.target.energy = self.target.max_energy
            self.source.session.say(f"💉|Энергия {self.target.name} восстановлена до максимальной! "
                                    f"({self.target.max_energy})")
