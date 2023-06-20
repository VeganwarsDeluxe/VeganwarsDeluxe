from core.Items.Item import DecisiveItem, FreeItem
from core.TargetType import Allies


class Adrenaline(FreeItem):
    def __init__(self, source):
        super().__init__(source, name='Адреналин', id='adrenaline', target_type=Allies())

    def use(self):
        self.target.energy += 3
        self.target.session.say(f'💉|{self.source.name} использует адреналин на {self.target.name}! '
                                f'Его енергия увеличена на 3.')
