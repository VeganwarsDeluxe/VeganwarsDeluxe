from core.Action import Action
from core.TargetType import TargetType


class Item(Action):  # TODO: Make your mind about implementation
    def __init__(self, name='Item', id='item', decisive=True, type=TargetType()):
        super().__init__(None, target_type=type, decisive=decisive, name=name, id=id)
        self.target = None
        self.priority = 5

    def __call__(self):
        if self.canceled:
            return
        self.use()

    def use(self):
        pass


class FreeItem(Item):
    def __init__(self, name='Item', id='item'):
        super().__init__(name=name, id=id, decisive=False)


class DecisiveItem(Item):
    def __init__(self, name='Item', id='item'):
        super().__init__(name=name, id=id, decisive=True)

