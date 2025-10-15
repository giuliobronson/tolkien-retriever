from core.application.ports.repositories.session_repository import ISessionRepository


class InMemorySessionRepository(ISessionRepository):
    def __init__(self):
        self.db = {}

    def find_by_id(self, id: int):
        return self.db[id]
