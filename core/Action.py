from core.TargetType import TargetType


class Action:
    def __init__(self, func, target_type, decisive=True, name='Action', id='action', priority=0):
        self.priority: int = priority  # TODO: Revise priorities of all actions
        self.decisive: bool = decisive
        self.name = name
        self.id = id
        self.func = func
        self.data = dict()

        self.target_type: TargetType = target_type

        self.source = None
        self.target = None

        self.canceled = False

    def __call__(self):  # Abstract "Run" method for overriding
        return self.func(self.source, self.target)

    @property
    def cost(self):
        return False


class DecisiveAction(Action):
    def __init__(self, func, target_type, name='Action', id='action', priority=0):
        super().__init__(func, target_type=target_type, decisive=True, name=name, id=id, priority=priority)

    @property
    def cost(self):
        return True


class FreeAction(Action):
    def __init__(self, func, name='Action', id='action', priority=0, type=TargetType()):
        super().__init__(func, target_type=type, decisive=False, name=name, id=id, priority=priority)

    @property
    def cost(self):
        return False