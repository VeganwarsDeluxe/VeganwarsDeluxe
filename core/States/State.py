class State:
    def __init__(self, source, id=None, name='None', constant=False, stage='pre-action'):
        self.source = source
        self.id = id
        self.name = name
        self.constant = constant
        self.stage = stage

    def is_triggered(self, stage):
        return self.constant or self.stage == stage

    @property
    def actions(self):
        return []

    def __call__(self, source):
        pass
