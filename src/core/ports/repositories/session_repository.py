from abc import abstractmethod
from typing import Optional

from core.domain.entities.session import Session
from core.ports.repositories.repository_port import RepositoryPort


class ISessionRepository(RepositoryPort[Session, str]):
    @abstractmethod
    async def find_by_rulebook_id(self, rulebook_id: str) -> Optional[Session]:
        pass
