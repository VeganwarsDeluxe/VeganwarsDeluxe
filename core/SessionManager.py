from core import Singleton
from core.Sessions.Session import Session


class SessionManager(Singleton):
    def __init__(self):
        self.sessions: list[Session] = []

        self.attached_event = lambda session_id: session_id

    def get_session(self, session_id):
        result = list(filter(lambda s: s.id == session_id, self.sessions))
        if result:
            return result[0]

    def attach_session(self, session: Session):
        self.sessions.append(session)
        self.attached_event(session.id)
        return session

    def delete_session(self, session_id):
        session = self.get_session(session_id)
        if session and session in self.sessions:
            self.sessions.remove(session)
