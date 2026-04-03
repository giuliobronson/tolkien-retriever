from typing import List

from core.domain.entities.rulebook import Rulebook
from core.domain.entities.session import Session
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.repositories.session_repository import ISessionRepository


class SessionService:
    def __init__(
        self,
        session_repository: ISessionRepository,
        rulebook_repository: IRulebookRepository,
    ) -> None:
        self.session_repository = session_repository
        self.rulebook_repository = rulebook_repository

    async def get_rulebooks_from_sessions(self) -> List[Rulebook]:
        sessions = await self.session_repository.find_all()
        rulebook_ids = list({session.rulebook_id for session in sessions})
        return await self.rulebook_repository.find_by_ids(rulebook_ids)

    async def create_session(self, rulebook_id: str) -> Session:
        return await self.session_repository.save(Session.create(rulebook_id))

    async def open_session(self, rulebook_id: str) -> Session:
        session = await self.session_repository.find_by_rulebook_id(rulebook_id)
        if session:
            return session
        return await self.create_session(rulebook_id)
