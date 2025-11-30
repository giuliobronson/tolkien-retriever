from abc import ABC, abstractmethod
from mailbox import Message
from typing import List
from core.domain.entities.document import Document


class IVectorDatabase(ABC):
    @abstractmethod
    async def add(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    async def similarity_search(self, query: Message, k: int = 5) -> List[Document]:
        pass

    @abstractmethod
    async def delete(self, doc_id: str) -> None:
        pass