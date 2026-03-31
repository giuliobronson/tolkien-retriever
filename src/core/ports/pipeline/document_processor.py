from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document


class IDocumentProcessor(ABC):

    @abstractmethod
    async def process(self, content: bytes, filename: str) -> List[Document]:
        pass
