from abc import ABC, abstractmethod
from typing import List

from core.domain.value_objects.message import Message


class IAgent(ABC):
    @abstractmethod
    def set_state(self, history: List[Message]) -> None:
        pass

    @abstractmethod
    async def answer(self, input: Message) -> Message:
        pass
