from abc import ABC, abstractmethod

from core.domain.entities.rulebook import Rulebook


class IRulebookPipeline(ABC):

    @abstractmethod
    async def execute(self, content: bytes, filename: str) -> None:
        pass
