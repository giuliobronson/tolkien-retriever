from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_DATABASE, MONGODB_URL
from infra.adapters.repositories.rulebook.mongodb_rulebook_repository import (
    MongoDBRulebookRepository,
)
from infra.adapters.repositories.session_repository.mongodb_session_repository import (
    MongoDBSessionRepository,
)


async def get_mongodb_client():
    client = AsyncIOMotorClient(MONGODB_URL)
    try:
        yield client
    finally:
        client.close()


async def get_session_repository(
    client: AsyncIOMotorClient = Depends(get_mongodb_client),
):
    db = client[MONGODB_DATABASE]
    repository = MongoDBSessionRepository(db)
    yield repository


async def get_rulebook_repository(
    client: AsyncIOMotorClient = Depends(get_mongodb_client),
):
    db = client[MONGODB_DATABASE]
    repository = MongoDBRulebookRepository(db)
    yield repository
