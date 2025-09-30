from abc import ABC, abstractmethod


class ISessionRepository(ABC):
    @abstractmethod
    def get_session(self, session_id: int):
        pass

    @abstractmethod
    def save_session(self, session):
        pass