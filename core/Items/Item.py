from core.Action import Action
from core.TargetType import TargetType


class Item(Action):  # TODO: Make your mind about implementation
    def __init__(self, source, name='Item', id='item', target_type=TargetType()):
        super().__init__(None, source, target_type=target_type, name=name, id=id)
        self.target = None
        self.priority = -1
        self.type = 'item'

    def __call__(self):
        if self.canceled:
            return
        self.source.session.event.item = self
        self.use()

    def use(self):
        pass

    @property
    def cost(self):
        return 1


class FreeItem(Item):
    def __init__(self, source, name='Item', id='item', target_type=TargetType()):
        super().__init__(source=source, name=name, id=id, target_type=target_type)

    @property
    def cost(self):
        return 0


class ImmediateItem(Item):
    def __init__(self, source, name='Item', id='item', target_type=TargetType()):
        super().__init__(source=source, name=name, id=id, target_type=target_type)

    @property
    def cost(self):
        return -1


class DecisiveItem(Item):
    def __init__(self, source, name='Item', id='item', target_type=TargetType()):
        super().__init__(source=source, name=name, id=id, target_type=target_type)

