from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from core.domain.entities.session import Session
from core.ports.repositories.session_repository import ISessionRepository
from infra.mappers.session_mapper import SessionMapper


class MongoDBSessionRepository(ISessionRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["sessions"]

    async def save(self, entity: Session) -> Session:
        data = SessionMapper.to_document(entity)
        await self.collection.replace_one({"id": entity.id}, data, upsert=True)
        return entity

    async def find_by_id(self, id: str) -> Optional[Session]:
        doc = await self.collection.find_one({"id": id})
        return SessionMapper.from_document(doc)

    async def find_by_rulebook_id(self, rulebook_id: str) -> Optional[Session]:
        doc = await self.collection.find_one({"rulebook_id": rulebook_id})
        return SessionMapper.from_document(doc)

    async def find_all(self) -> List[Session]:
        cursor = self.collection.find({})
        docs = await cursor.to_list(length=None)
        return [
            s for doc in docs if (s := SessionMapper.from_document(doc)) is not None
        ]

    async def update(self, id: str, entity: Session) -> Session:
        data = SessionMapper.to_document(entity)
        await self.collection.update_one({"id": id}, {"$set": data})
        return entity

    async def delete(self, id: str) -> None:
        await self.collection.delete_one({"id": id})
