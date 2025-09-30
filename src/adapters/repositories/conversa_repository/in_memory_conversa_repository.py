from ports.repositories.session_repository import ISessionRepository


class InMemorySessionRepository(ISessionRepository):
    def get_session(self, session_id: int):
        pass
