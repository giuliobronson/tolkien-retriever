from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.rulebook import Rulebook
from core.ports.repositories.repository_port import RepositoryPort


class IRulebookRepository(RepositoryPort[Rulebook, str]):
    @abstractmethod
    async def find_by_hash(self, hash: str) -> Optional[Rulebook]:
        pass

    @abstractmethod
    async def find_by_ids(self, ids: List[str]) -> List[Rulebook]:
        pass
