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
        try:
            await self.collection.insert_one(rulebook_dict)
            return entity
        except Exception:
            raise  # Raise mesmo ou trata aqui?

    async def find_by_id(self, id: str) -> Optional[Rulebook]:
        try:
            result = await self.collection.find_one({"hash": id})
            return RulebookMapper.document_to_entity(result) if result else None
        except ValueError:
            raise  # Erro de conexão
        except Exception:
            return None  # Not found

    async def find_all(self) -> List[Rulebook]:
        results = await self.collection.find({}).to_list(None)
        return [RulebookMapper.document_to_entity(doc) for doc in results]

    async def update(self, id: str, entity: Rulebook) -> Rulebook:
        rulebook_dict = RulebookMapper.entity_to_document(entity)
        try:
            await self.collection.update_one({"hash": id}, {"$set": rulebook_dict})
            return entity
        except:
            raise  # Raise mesmo ou trata aqui?

    async def delete(self, id: str) -> None:
        try:
            await self.collection.delete_one({"hash": id})
        except Exception:
            pass
