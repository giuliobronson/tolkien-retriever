from fastapi import Depends
from adapters.llm.langgraph_agent import LangGraphAgent
from adapters.llm.langgraph_builder import LangGraphBuilder
from adapters.repositories.session_repository.in_memory_session_repository import InMemorySessionRepository
from core.application.services.chat_service import ChatService
from core.application.services.session_service import SessionService
from core.ports.llm.agent import IAgent
from core.ports.repositories.session_repository import ISessionRepository


async def get_session_repository():
    repository = InMemorySessionRepository()
    yield repository
    
async def get_session_service(repository: ISessionRepository=Depends(get_session_repository)):
    service = SessionService(repository)
    yield service

async def get_graph_builder():
    builder = LangGraphBuilder()
    yield builder

async def get_agent(graph_builder: LangGraphBuilder=Depends(get_graph_builder)):
    agent = LangGraphAgent(graph_builder.build_graph())
    yield agent

async def get_chat_service(repository: ISessionRepository=Depends(get_session_repository), agent: IAgent=Depends(get_agent)):
    service = ChatService(repository, agent)
    yield service