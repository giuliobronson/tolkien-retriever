from abc import ABC, abstractmethod


class IAgentGraph(ABC):
    @abstractmethod
    def _build_graph(self):
        pass

    @abstractmethod
    def run(self, input: str) -> str:
        pass
