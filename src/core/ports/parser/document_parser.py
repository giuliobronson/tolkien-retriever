from abc import ABC, abstractmethod


class IDocumentParser(ABC):
    @abstractmethod
    def extract_text(self, content: bytes) -> str:
        """Extrai texto do documento."""
        pass
