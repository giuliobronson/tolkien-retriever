from abc import ABC, abstractmethod
from typing import Optional


class IFileStorage(ABC):
    @abstractmethod
    def upload(self, path: str, content: bytes, content_type: Optional[str]) -> None:
        """Envia um arquivo para o storage."""
        pass

    @abstractmethod
    def download(self, path: str) -> bytes:
        """Baixa um arquivo do storage."""
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Verifica se o arquivo existe no storage."""
        pass
