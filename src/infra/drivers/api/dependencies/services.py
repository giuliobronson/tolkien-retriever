from fastapi import Depends

from core.application.services.chat_service import ChatService
from core.application.services.rulebook_service import RulebookService
from core.application.services.session_service import SessionService
from core.ports.llm.agent import IAgent
from core.ports.pipeline.rulebook_pipeline import IRulebookPipeline
from core.ports.repositories.rulebook_repository import IRulebookRepository
from core.ports.repositories.session_repository import ISessionRepository
from core.ports.storage.file_storage import IFileStorage
from infra.drivers.api.dependencies.agents import get_agent
from infra.drivers.api.dependencies.pipeline import get_rulebook_pipeline
from infra.drivers.api.dependencies.repositories import (
    get_rulebook_repository,
    get_session_repository,
)
from infra.drivers.api.dependencies.storage import get_file_storage


async def get_session_service(
    repository: ISessionRepository = Depends(get_session_repository),
):
    service = SessionService(repository)
    yield service


async def get_chat_service(
    repository: ISessionRepository = Depends(get_session_repository),
    agent: IAgent = Depends(get_agent),
):
    service = ChatService(repository, agent)
    yield service


async def get_rulebook_service(
    storage: IFileStorage = Depends(get_file_storage),
    processer: IRulebookPipeline = Depends(get_rulebook_pipeline),
    repository: IRulebookRepository = Depends(get_rulebook_repository),
):
    service = RulebookService(storage, processer, repository)
    yield service
