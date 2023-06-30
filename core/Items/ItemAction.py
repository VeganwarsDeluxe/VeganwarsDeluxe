from core.Actions.Action import Action


class ItemAction(Action):
    id = 'item'
    name = 'Item'

    def __init__(self, source, target_type, priority=-1):
        super().__init__(source, target_type=target_type, priority=priority)
        self.target = target_type
        self.priority = priority
        self.type = 'item'


class FreeItem(ItemAction):
    @property
    def cost(self):
        return 0


class DecisiveItem(ItemAction):
    @property
    def cost(self):
        return 1
