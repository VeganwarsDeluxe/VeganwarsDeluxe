from core import SessionManager, Session, Entity
from core.Actions.ActionManager import ActionManager
from core.ContentManager import content_manager
from core.Events.EventManager import EventManager
from core.States import State


class Engine:
    def __init__(self):
        self.event_manager = EventManager()
        self.session_manager = SessionManager(self.event_manager)
        self.action_manager = ActionManager(self.session_manager, action_map=content_manager.action_map)

        content_manager.initialize_action_manager(self.action_manager)
        content_manager.attach_action_manager(self.action_manager)

    def attach_session(self, session: Session):
        self.session_manager.attach_session(session)

    def detach_session(self, session: Session):
        self.session_manager.delete_session(session.id)
        self.event_manager.clean_by_session_id(session.id)

    def attach_states(self, entity: Entity, state_pool: list[type[State]]):
        for state in state_pool:
            entity.attach_state(state(), self.event_manager)

    def stats(self):
        result = (f"Event Handlers: {self.event_manager.size}\n"
                  f"Sessions: {len(self.session_manager.sessions)}\n"
                  f"Action Queue: {len(self.action_manager.action_queue)}\n")
        return result
