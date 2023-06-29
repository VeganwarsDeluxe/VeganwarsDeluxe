from core import Singleton
from core.Sessions.Session import Session


class SessionManager(Singleton):
    def __init__(self):
        self.sessions: list[Session] = []

    def get_session(self, session_id: int):
        return list(filter(lambda s: s.id == session_id, self.sessions))[0]

    def create_session(self):
        session = Session()
        self.sessions.append(session)
        return session
