from typing import List, Optional

from core.domain.entities.session import Session
from core.ports.repositories.session_repository import ISessionRepository


class InMemorySessionRepository(ISessionRepository):
    db = {}

    async def save(self, entity: Session) -> Session:
        self.db[entity.id] = entity
        return entity

    async def find_by_id(self, id: str) -> Optional[Session]:
        if id not in self.db.keys():
            return None
        return self.db[id]

    async def find_all(self) -> List[Session]:
        return list(self.db.values())

    async def find_by_rulebook_id(self, rulebook_id: str) -> Optional[Session]:
        return next(
            (s for s in self.db.values() if s.rulebook_id == rulebook_id), None
        )

    async def update(self, id: str, entity: Session) -> Session:
        self.db[id] = entity
        return entity

    async def delete(self, id: str) -> None:
        self.db.pop(id)
