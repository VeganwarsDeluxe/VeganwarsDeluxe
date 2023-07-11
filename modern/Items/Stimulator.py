from core.Actions.ActionManager import AttachedAction
from core.Items.Item import Item
from core.Actions.ItemAction import DecisiveItem
from core.TargetType import Allies


class Stimulator(Item):
    id = 'stimulator'
    name = 'Стимулятор'


@AttachedAction(Stimulator)
class StimulatorAction(DecisiveItem):
    id = 'stimulator'
    name = 'Стимулятор'
    target_type = Allies()
    priority = -2

    def func(self, source, target):
        target.hp = min(target.hp + 2, target.max_hp)
        self.session.say(f'💉|{source.name} использует стимулятор на {target.name}!')
        self.session.say(f'{target.hearts}💉|{target.name} получает 2 хп. Остается {target.hp} хп.')
