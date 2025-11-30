from core.ports.repositories.session_repository import ISessionRepository


class MongoDBSessionRepository(ISessionRepository):
    def __init__(self, uri: str, db_name: str, collection_name: str = "sessions"):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    # -------------------------------
    # HELPERS
    # -------------------------------
    @staticmethod
    def _to_object_id(id: str):
        try:
            return ObjectId(id)
        except Exception:
            raise ValueError(f"Invalid ObjectId: {id}")

    @staticmethod
    def _normalize(doc) -> Optional[Session]:
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return Session(**doc)

    @staticmethod
    def _serialize(entity: Session) -> dict:
        data = entity.model_dump()
        if "id" in data and data["id"]:
            data["_id"] = ObjectId(data["id"])
        data.pop("id", None)
        return data

    # -------------------------------
    # CRUD
    # -------------------------------
    async def save(self, entity: Session) -> Session:
        data = self._serialize(entity)

        if "_id" in data:
            # update
            await self.collection.replace_one({"_id": data["_id"]}, data, upsert=True)
            doc = await self.collection.find_one({"_id": data["_id"]})
            return self._normalize(doc)
        else:
            # insert
            result = await self.collection.insert_one(data)
            doc = await self.collection.find_one({"_id": result.inserted_id})
            return self._normalize(doc)

    async def find_by_id(self, id: str) -> Optional[Session]:
        oid = self._to_object_id(id)
        doc = await self.collection.find_one({"_id": oid})
        return self._normalize(doc)

    async def find_all(self) -> List[Session]:
        cursor = self.collection.find({})
        docs = await cursor.to_list(length=None)
        return [self._normalize(doc) for doc in docs]

    async def delete(self, id: str) -> None:
        oid = self._to_object_id(id)
        await self.collection.delete_one({"_id": oid})