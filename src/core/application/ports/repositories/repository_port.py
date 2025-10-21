from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")
I = TypeVar("I")

class RepositoryPort(ABC, Generic[T, I]):
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass
    
    @abstractmethod
    async def find_by_id(self, id: I) -> Optional[T]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[T]:
        pass
    
    @abstractmethod
    async def delete(self, id: I) -> None:
        pass