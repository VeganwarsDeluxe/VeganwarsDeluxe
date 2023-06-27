from core.Action import Action
from core.TargetType import TargetType


class Item(Action):
    id = 'item'
    name = 'Item'

    def __init__(self, source, target_type=TargetType(), priority=-1):
        super().__init__(source, target_type=target_type, priority=priority)
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
    def __init__(self, source, target_type=TargetType(), priority=-1):
        super().__init__(source, target_type=target_type, priority=priority)

    @property
    def cost(self):
        return 0


class ImmediateItem(Item):
    def __init__(self, source, target_type=TargetType(), priority=-1):
        super().__init__(source, target_type=target_type, priority=priority)

    @property
    def cost(self):
        return -1


class DecisiveItem(Item):
    def __init__(self, source, target_type=TargetType(), priority=-1):
        super().__init__(source, target_type=target_type, priority=priority)
