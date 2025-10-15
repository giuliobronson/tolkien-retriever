from typing import Optional
from core.application.ports.repositories.session_repository import ISessionRepository
from core.domain.entities.message import Message
from core.domain.entities.session import Session


class SessionService:
    def __init__(self, session_repository: ISessionRepository) -> None:
        self.session_repository = session_repository
        
    async def save_message(self, session_id: int, message: Message) -> Message:
        session: Optional[Session] = await self.session_repository.find_by_id(session_id)
        if not session:
            session.messages.append(message)
        return message