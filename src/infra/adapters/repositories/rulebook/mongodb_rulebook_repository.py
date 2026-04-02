from typing import List, Optional

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.domain.entities.rulebook import Rulebook
from core.ports.repositories.rulebook_repository import IRulebookRepository
from infra.mappers.rulebook_mapper import RulebookMapper


class MongoDBRulebookRepository(IRulebookRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["rulebooks"]

    async def save(self, entity: Rulebook) -> Rulebook:
        rulebook_dict = RulebookMapper.entity_to_document(entity)
        await self.collection.insert_one(rulebook_dict)
        return entity

    async def find_by_id(self, id: str) -> Optional[Rulebook]:
        result = await self.collection.find_one({"id": id})
        return RulebookMapper.document_to_entity(result) if result else None

    async def find_by_hash(self, hash: str) -> Optional[Rulebook]:
        result = await self.collection.find_one({"hash": hash})
        return RulebookMapper.document_to_entity(result) if result else None

    async def find_all(self) -> List[Rulebook]:
        results = await self.collection.find({}).to_list(None)
        return [RulebookMapper.document_to_entity(doc) for doc in results]

    async def update(self, id: str, entity: Rulebook) -> Rulebook:
        rulebook_dict = RulebookMapper.entity_to_document(entity)
        await self.collection.update_one({"id": id}, {"$set": rulebook_dict})
        return entity

    async def delete(self, id: str) -> None:
        await self.collection.delete_one({"id": id})
