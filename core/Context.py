from core.Sessions import Session


class Context[T]:
    def __init__(self, event: T, session: Session):
        self.event: T = event
        self.session = session