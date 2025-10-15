from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")

class RepositoryPort(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass
    
    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[T]:
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> None:
        pass