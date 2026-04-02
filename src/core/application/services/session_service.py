from core.domain.entities.session import Session
from core.ports.repositories.session_repository import ISessionRepository


class SessionService:
    def __init__(self, session_repository: ISessionRepository) -> None:
        self.session_repository = session_repository

    async def create_session(self, rulebook_id: str) -> Session:
        return await self.session_repository.save(Session.create(rulebook_id))

    async def open_session(self, rulebook_id: str) -> Session:
        session = await self.session_repository.find_by_rulebook_id(rulebook_id)
        if session:
            return session
        return await self.create_session(rulebook_id)
