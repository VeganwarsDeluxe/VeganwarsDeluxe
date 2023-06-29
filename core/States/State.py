from core.Events import EventManager
from core.Message import Message, PreActionsMessage


class State:
    id = None
    name = 'None'

    def __init__(self, source):
        self.source = source
        self.event_manager = EventManager()

    def register(self, session_id):
        pass

    @property
    def actions(self):
        return []
