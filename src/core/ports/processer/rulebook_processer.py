from abc import ABC, abstractmethod

from core.domain.entities.rulebook import Rulebook


class IRulebookProcesser(ABC):

    @abstractmethod
    async def process(self, content: bytes, filename: str) -> None:
        pass
