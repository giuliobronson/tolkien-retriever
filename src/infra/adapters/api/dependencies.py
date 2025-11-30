from fastapi import Depends
from langchain.chat_models import init_chat_model
from qdrant_client import QdrantClient

from infra.adapters.llm.factories.base_chat_factory import BaseChatFactory
from infra.adapters.llm.factories.rag_factory import RagFactory
from infra.adapters.repositories.session_repository.in_memory_session_repository import InMemorySessionRepository
from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.ports.llm.agent import IAgent
from core.ports.repositories.session_repository import ISessionRepository
from config import MINIO_ENDPOINT_URL, MINIO_ROOT_PASSWORD, MINIO_ROOT_USER, OPENAI_API_KEY
from infra.adapters.storage.MinIOStorage import MinIOStorage


async def get_session_repository():
    repository = InMemorySessionRepository()
    yield repository
    
async def get_session_service(repository: ISessionRepository=Depends(get_session_repository)):
    service = SessionService(repository)
    yield service

async def get_base_chat_agent():
    agent_factory = BaseChatFactory(
        init_chat_model(
            model="gpt-4o-mini", 
            model_provider="openai", 
            api_key=OPENAI_API_KEY, 
            temperature=0.7
        )
    )
    agent = agent_factory.create_agent()
    yield agent

async def get_rag_agent():
    agent_factory = RagFactory(
        init_chat_model(
            model="gpt-4o-mini", 
            model_provider="openai", 
            api_key=OPENAI_API_KEY, 
            temperature=0.7
        ),
        QdrantClient()
    )
    agent = agent_factory.create_agent()
    yield agent

async def get_chat_service(repository: ISessionRepository=Depends(get_session_repository), agent: IAgent=Depends(get_base_chat_agent)):
    service = ChatService(repository, agent)
    yield service

async def get_rag_service(repository: ISessionRepository=Depends(get_session_repository), agent: IAgent=Depends(get_rag_agent)):
    service = ChatService(repository, agent)
    yield service

async def get_file_storage():
    return MinIOStorage(
        endpoint=MINIO_ENDPOINT_URL, 
        access_key=MINIO_ROOT_USER,
        secret_key=MINIO_ROOT_PASSWORD,
        bucket_name="documents",
        secure=False
    )