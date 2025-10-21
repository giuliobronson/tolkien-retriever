from adapters.api.dto.session_dto import SessionDTO
from adapters.mappers.message_mapper import MessageMapper
from core.domain.entities.session import Session


class SessionMapper:
    @staticmethod
    def to_dto(session: Session) -> SessionDTO:
        return SessionDTO(
            id=session.id,
            title=session.title,
            messages=[MessageMapper.to_dto(message) for message in session.messages]
        )

    @staticmethod
    def to_entity(session_dto: SessionDTO) -> Session:
        return Session(
            id=session_dto.id,
            title=session_dto.title,
            messages=[MessageMapper.to_entity(message) for message in session_dto.messages]
        )