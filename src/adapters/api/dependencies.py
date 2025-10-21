from fastapi import Depends
from adapters.repositories.session_repository.in_memory_session_repository import InMemorySessionRepository
from core.application.ports.repositories.session_repository import ISessionRepository
from core.application.services.session_service import SessionService


async def get_session_repository():
    repository = InMemorySessionRepository()
    yield repository
    
async def get_session_service(repository: ISessionRepository=Depends(get_session_repository)):
    service = SessionService(repository)
    yield service