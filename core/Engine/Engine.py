from core import SessionManager
from core.Actions.ActionManager import ActionManager
from core.ContentManager import content_manager
from core.Events.EventManager import EventManager


class Engine:
    def __init__(self):
        self.event_manager = EventManager()
        self.session_manager = SessionManager(self.event_manager)
        self.action_manager = ActionManager(self.session_manager, action_map=content_manager.action_map)

        content_manager.initialize_action_manager(self.action_manager)
        content_manager.attach_action_manager(self.action_manager)

