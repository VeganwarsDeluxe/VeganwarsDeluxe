from core.Sessions.Session import Session


class SessionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.sessions: list[Session] = []

    def get_session(self, session_id: int):
        return list(filter(lambda s: s.id == session_id, self.sessions))[0]

    def create_session(self):
        session = Session()
        self.sessions.append(session)
        return session
