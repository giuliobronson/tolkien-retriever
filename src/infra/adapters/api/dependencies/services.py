from fastapi import Depends
from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.ports.llm.agent import IAgent
from core.ports.repositories.session_repository import ISessionRepository
from infra.adapters.api.dependencies.agents import get_base_chat_agent
from infra.adapters.api.dependencies.repositories import get_session_repository


async def get_session_service(repository: ISessionRepository=Depends(get_session_repository)):
    service = SessionService(repository)
    yield service

async def get_chat_service(repository: ISessionRepository=Depends(get_session_repository), agent: IAgent=Depends(get_base_chat_agent)):
    service = ChatService(repository, agent)
    yield service

async def get_rag_service(repository: ISessionRepository=Depends(get_session_repository), agent: IAgent=Depends(get_base_chat_agent)):
    service = ChatService(repository, agent)
    yield service