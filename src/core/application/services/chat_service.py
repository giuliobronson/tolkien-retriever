from typing import Optional
from core.application.ports.repositories.session_repository import ISessionRepository
from core.domain.entities.message import Message
from core.domain.entities.session import Session
from core.domain.exceptions.session_not_found_error import SessionNotFoundError


class ChatService:
    def __init__(self, session_repository: ISessionRepository, agent) -> None:
        self.session_repository = session_repository
        self.agent = agent
        
    async def handle_query(self, session: Session, query: Message) -> Message:
        response: Message = self.agent.answer(session.messages, query)
        session.messages.extend([query, response])
        await self.session_repository.save(session)
        return response
        