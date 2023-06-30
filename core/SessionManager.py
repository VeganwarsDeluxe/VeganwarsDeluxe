from core import Singleton
from core.Events.EventManager import EventManager
from core.Events.Events import AttachSessionEvent
from core.Sessions.Session import Session


class SessionManager(Singleton):
    def __init__(self):
        self.sessions: list[Session] = []
        self.event_manager = EventManager()

    def get_session(self, session_id):
        result = list(filter(lambda s: s.id == session_id, self.sessions))
        if result:
            return result[0]

    def attach_session(self, session: Session):
        self.sessions.append(session)
        self.event_manager.publish(AttachSessionEvent(session.id))
        return session

    def delete_session(self, session_id):
        session = self.get_session(session_id)
        if session and session in self.sessions:
            self.sessions.remove(session)
