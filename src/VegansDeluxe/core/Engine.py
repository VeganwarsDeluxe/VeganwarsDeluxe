from VegansDeluxe.core import Session, Entity
from VegansDeluxe.core.Actions.ActionManager import ActionManager
from VegansDeluxe.core.ContentManager import content_manager
from VegansDeluxe.core.Events.EventManager import EventManager
from VegansDeluxe.core.SessionManager import SessionManager
from VegansDeluxe.core.States import State


class Engine:
    def __init__(self):
        """
        Engine class, that puts all content and managers together, ready for work.
        """

        self.event_manager: EventManager = EventManager()
        self.session_manager: SessionManager = SessionManager(self.event_manager)
        self.action_manager: ActionManager = ActionManager(self.session_manager, action_map=content_manager.action_map)

        content_manager.attach_action_manager(self.action_manager)

    async def attach_session(self, session: Session):
        await self.session_manager.attach_session(session)

    def detach_session(self, session: Session):
        self.session_manager.delete_session(session.id)
        self.event_manager.clean_by_session_id(session.id)

    async def attach_states(self, entity: Entity, state_pool: list[type[State]]):
        for state in state_pool:
            await entity.attach_state(state(), self.event_manager)

    def stats(self):
        result = (f"Event Handlers: {self.event_manager.size}\n"
                  f"Sessions: {len(self.session_manager.sessions)}\n"
                  f"Action Queue: {len(self.action_manager.action_queue)}\n"
                  f"CM Assignments: {len(content_manager.assignments)}")
        return result
