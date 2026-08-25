# Feature module: only imports leaf modules (repositories/storage/pipeline/agents) — never another feature module in dependencies/.
from fastapi import Depends

from core.application.services.chat_service import ChatService
from core.ports.llm.agent import IAgent
from core.ports.repositories.session_repository import ISessionRepository
from infra.drivers.api.dependencies.agents import get_agent
from infra.drivers.api.dependencies.repositories import get_session_repository


async def get_chat_service(
    repository: ISessionRepository = Depends(get_session_repository),
    agent: IAgent = Depends(get_agent),
):
    service = ChatService(repository, agent)
    yield service
