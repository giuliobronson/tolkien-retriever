from typing import Optional

from core.domain.entities.session import Session
from infra.drivers.api.dto.session_dto import SessionDTO
from infra.mappers.message_mapper import MessageMapper


class SessionMapper:
    @staticmethod
    def to_document(session: Session) -> dict:
        return {
            "id": session.id,
            "rulebook_id": session.rulebook_id,
            "messages": [MessageMapper.to_document(m) for m in session.messages],
        }

    @staticmethod
    def from_document(doc: Optional[dict]) -> Optional[Session]:
        if not doc:
            return None
        return Session(
            id=doc["id"],
            rulebook_id=doc["rulebook_id"],
            messages=[MessageMapper.from_document(m) for m in doc.get("messages", [])],
        )

    @staticmethod
    def to_dto(session: Session) -> SessionDTO:
        return SessionDTO(
            id=session.id,
            rulebook_id=session.rulebook_id,
            messages=[MessageMapper.to_dto(message) for message in session.messages],
        )

    @staticmethod
    def to_entity(session_dto: SessionDTO) -> Session:
        return Session(
            id=session_dto.id,
            rulebook_id=session_dto.rulebook_id,
            messages=[
                MessageMapper.to_entity(message) for message in session_dto.messages
            ],
        )
