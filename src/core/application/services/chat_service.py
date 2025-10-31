from core.domain.exceptions.no_active_session_error import NoActiveSessionError
from core.ports.llm.agent import IAgent
from core.ports.repositories.session_repository import ISessionRepository
from core.domain.value_objects.message import Message
from core.domain.entities.session import Session


class ChatService:
    def __init__(self, session_repository: ISessionRepository, agent: IAgent) -> None:
        self.session_repository = session_repository
        self.agent = agent
        self.current_session = None

    def load_session(self, session: Session) -> None:
        self.current_session = session
        self.agent.set_state(session.messages)
        
    async def answer(self, query: Message) -> Message:
        response = await self.agent.answer(query)
        if not self.current_session:
            raise NoActiveSessionError()
        self.current_session.messages.extend([query, response])
        await self.session_repository.save(self.current_session)
        return response
        