from abc import ABC, abstractmethod

from core.ports.llm.agent import IAgent


class IAgentFactory(ABC):
    @abstractmethod
    def create(self) -> IAgent:
        pass