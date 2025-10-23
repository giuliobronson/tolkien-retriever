import datetime
from core.application.ports.llm.agent_graph import IAgentGraph
from core.application.ports.repositories.session_repository import ISessionRepository
from core.domain.value_objects.author import Author
from core.domain.value_objects.message import Message
from core.domain.entities.session import Session


class ChatService:
    def __init__(self, session_repository: ISessionRepository, agent_graph: IAgentGraph) -> None:
        self.session_repository = session_repository
        self.current_session = None
        self.agent_graph = agent_graph

    def load_session(self, session: Session) -> None:
        self.current_session = session
        
    async def answer(self, query: Message) -> Message:
        response = await self.chain.ainvoke({"input": query.content})
        answer = Message(
            author=Author(role="agent"),
            content=query.content,
            timestamp=datetime.datetime.now(),
        )
        response: Message = await self.agent_service.answer(self.current_session.messages, query)
        self.current_session.messages.extend([query, response])
        await self.session_repository.save(self.current_session)
        return response
        