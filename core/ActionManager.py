from core import Singleton
from core.Action import Action
from core.Events.EventManager import EventManager
from core.Events.Events import CallActionsEvent
from core.Items import Item
from core.SessionManager import SessionManager


class ActionManager(Singleton):
    def __init__(self):
        self.action_queue: list[Action] = []
        self.item_queue: list[Item] = []

        self.actions: list[Action] = []
        self.session_manager = SessionManager()
        self.event_manager = EventManager()
        self.session_manager.attached_event = self.register

    def add_action(self, action: Action):
        self.actions.append(action)

    def queue_action(self, action_id: str) -> bool:
        action = list(filter(lambda a: action_id == a.id, self.actions))[0]
        return not action.cost

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=CallActionsEvent)
        def func(message: CallActionsEvent):
            for action in self.action_queue:
                if action.session.id != session_id:
                    continue
                action()
