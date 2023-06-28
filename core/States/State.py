class State:
    id = None
    name = 'None'

    def __init__(self, source, constant=False, stage='pre-action'):
        self.source = source
        self.constant = constant
        self.stage = stage

    def register(self):
        pass

    def is_triggered(self, message):
        return self.constant or self.stage == message.current_event

    @property
    def actions(self):
        return []
