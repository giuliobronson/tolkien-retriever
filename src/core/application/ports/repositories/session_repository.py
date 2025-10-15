from abc import ABC, abstractmethod


class ISessionRepository(ABC):
    @abstractmethod
    def get_by_id(self, session_id: int):
        pass