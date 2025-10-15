from typing import List
from core.application.ports.repositories.message_repository import IMessageRepository
from core.domain.entities.message import Message


class InMemoryMessageRepository(IMessageRepository):
    def __init__(self):
        self.db = []

    def get_all(self) -> List[Message]:
        return self.db

    async def save(self, entity: Message) -> Message:
        self.db.append(entity)
        return entity