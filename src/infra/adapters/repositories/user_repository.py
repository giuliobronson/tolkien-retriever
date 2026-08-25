from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from core.domain.entities.user import User
from core.ports.repositories.user_repository import IUserRepository
from infra.mappers.user_mapper import UserMapper


class MongoDBUserRepository(IUserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def save(self, entity: User) -> User:
        data = UserMapper.to_document(entity)
        await self.collection.replace_one({"uid": entity.uid}, data, upsert=True)
        return entity

    async def find_by_id(self, id: str) -> Optional[User]:
        doc = await self.collection.find_one({"uid": id})
        return UserMapper.from_document(doc)

    async def find_all(self) -> List[User]:
        cursor = self.collection.find({})
        docs = await cursor.to_list(length=None)
        return [u for doc in docs if (u := UserMapper.from_document(doc)) is not None]

    async def update(self, id: str, entity: User) -> User:
        data = UserMapper.to_document(entity)
        await self.collection.update_one({"uid": id}, {"$set": data})
        return entity

    async def delete(self, id: str) -> None:
        await self.collection.delete_one({"uid": id})
