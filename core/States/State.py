from core.Events.EventManager import EventManager


class State:
    id = None
    name = 'None'

    def __init__(self, source):
        self.source = source
        self.event_manager = EventManager()

    def register(self, session_id):
        pass
