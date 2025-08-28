from abc import ABC, abstractmethod
from typing import Any

from domain.conversa import Conversa


class ConversaRepository(ABC):
    @abstractmethod
    async def get(self, **filters: Any) -> Conversa | None:
        pass 