class Action:
    def __init__(self, func, decisive=True, priority=0, name='Action', id='action'):
        self.priority: int = priority
        self.decisive: bool = decisive
        self.name = name
        self.id = id
        self.func = func
        self.data = dict()

        self.source = None
        self.target = None

        self.canceled = False

    def __call__(self):  # Abstract "Run" method for overriding
        return self.func(self.source, self.target)


class DecisiveAction(Action):
    def __init__(self, func, name='Action', id='action', priority=0):
        super().__init__(func, decisive=True, name=name, id=id, priority=priority)


class FreeAction(Action):
    def __init__(self, func, name='Action', id='action', priority=0):
        super().__init__(func, decisive=False, name=name, id=id, priority=priority)

