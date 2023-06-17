from core.Items.Item import DecisiveItem
from core.TargetType import Allies


class Stimulator(DecisiveItem):
    def __init__(self, source):
        super().__init__(source, name='Стимулятор', id='stimulator', target_type=Allies())

    def use(self):
        self.target.hp += 2
        self.target.session.say(f'💉|{self.source.name} использует стимулятор на {self.target.name}!')
        self.target.session.say(f'{self.target.hearts}💉|{self.target.name} получает 2 хп. Остается {self.target.hp} хп.')
