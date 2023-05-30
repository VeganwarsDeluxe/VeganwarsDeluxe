class Action:
    def __init__(self, func, decisive=True, priority=0, name='Action', id='action'):
        self.priority: int = priority
        self.decisive: bool = decisive
        self.name = name
        self.id = id
        self.func = func

    def __call__(self, source, target):  # Abstract "Run" method for overriding
        return self.func(source, target)


class DecisiveAction(Action):
    def __init__(self, func, name='Action', id='action'):
        super().__init__(func, decisive=True, priority=3, name=name, id=id)


class FreeAction(Action):
    def __init__(self, func, name='Action', id='action'):
        super().__init__(func, decisive=False, name=name, id=id)
