from abc import ABC, abstractmethod
from typing import List
from core.domain.entities.message import Message


class IMessageRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Message]:
        pass

    @abstractmethod
    def save(self, message: Message) -> Message:
        pass