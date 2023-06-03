from core.Items.Item import DecisiveItem


class Stimulator(DecisiveItem):
    def __init__(self):
        super().__init__(name='Стимулятор', id='stimulator')

    def use(self):
        self.target.hp += 2
        self.target.say(f'Я получаю 2 хп от стимулятора! Теперь у меня {self.target.hp} ХП.')
