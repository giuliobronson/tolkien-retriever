from typing import AsyncIterator

from core.domain.entities.session import Session
from core.domain.value_objects.message import Message
from core.ports.llm.agent import IAgent
from core.ports.repositories.session_repository import ISessionRepository


class ChatService:
    def __init__(self, session_repository: ISessionRepository, agent: IAgent) -> None:
        self.session_repository = session_repository
        self.agent = agent
        self.current_session = None

    def load_session(self, session: Session) -> None:
        self.current_session = session
        self.agent.set_history(session.messages)

    async def answer(self, query: Message) -> Message:
        assert self.current_session is not None
        response = await self.agent.answer(query)
        self.current_session.messages = self.agent.get_history()
        await self.session_repository.save(self.current_session)
        return response

    async def answer_stream(self, query: Message) -> AsyncIterator[str]:
        assert self.current_session is not None
        async for token in self.agent.answer_stream(query):
            yield token
        self.current_session.messages = self.agent.get_history()
        await self.session_repository.save(self.current_session)
