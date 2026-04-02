from abc import abstractmethod
from typing import Optional

from core.domain.entities.rulebook import Rulebook
from core.ports.repositories.repository_port import RepositoryPort


class IRulebookRepository(RepositoryPort[Rulebook, str]):
    @abstractmethod
    async def find_by_hash(self, hash: str) -> Optional[Rulebook]:
        raise NotImplementedError
