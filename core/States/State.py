class State:
    id = None
    name = 'None'

    def __init__(self, source, constant=False, stage='pre-action'):
        self.source = source
        self.constant = constant
        self.stage = stage

    def is_triggered(self, stage):
        return self.constant or self.stage == stage

    @property
    def actions(self):
        return []

    def __call__(self):
        pass
