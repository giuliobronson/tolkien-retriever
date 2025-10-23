from typing import Optional
from core.application.ports.repositories.session_repository import ISessionRepository
from core.domain.value_objects.message import Message
from core.domain.entities.session import Session
from core.domain.exceptions.session_not_found_error import SessionNotFoundError


class SessionService:
    def __init__(self, session_repository: ISessionRepository) -> None:
        self.session_repository = session_repository
        
    async def open_session(self, session_id: str):
        session: Optional[Session] = await self.session_repository.find_by_id(session_id)
        if not session:
            raise SessionNotFoundError(session_id)
        return session
    
    async def create_session(self, message: Message) -> Session:
        title = "Título Teste"
        return Session.create(title, message)
        
    async def save_message(self, session_id: str, message: Message) -> Message:
        session: Optional[Session] = await self.session_repository.find_by_id(session_id)
        if not session:
            raise SessionNotFoundError(session_id)
        session.messages.append(message)
        return message