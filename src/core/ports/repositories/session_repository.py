from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.session import Session
from core.ports.repositories.repository_port import RepositoryPort


class ISessionRepository(RepositoryPort[Session, str]):
    @abstractmethod
    async def find_by_rulebook_id_and_owner(
        self, rulebook_id: str, owner_id: str
    ) -> Optional[Session]:
        pass

    @abstractmethod
    async def find_all_by_owner_id(self, owner_id: str) -> List[Session]:
        pass
