from core.application.ports.repositories.session_repository import ISessionRepository


class InMemorySessionRepository(ISessionRepository):
    def __init__(self):
        self.db = {}

    def get_by_id(self, session_id: int):
        return self.db[session_id]
