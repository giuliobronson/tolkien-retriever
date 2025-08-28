from typing import Any
from domain.conversa import Conversa
from ports.repositories.conversa_repository import ConversaRepository


class InMemoryConversaRepository(ConversaRepository):
    async def get(self, **filters: Any) -> Conversa | None:
        pass
