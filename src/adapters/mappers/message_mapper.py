from adapters.api.dto.message_dto import MessageDTO
from adapters.mappers.author_mapper import AuthorMapper
from core.domain.entities.message import Message


class MessageMapper:
    @staticmethod
    def to_dto(message: Message) -> MessageDTO:
        return MessageDTO(
            author=AuthorMapper.to_dto(message.author),
            content=message.content,
            timestamp=message.timestamp
        )

    @staticmethod
    def to_entity(message_dto: MessageDTO):
        return Message(
            author=AuthorMapper.to_entity(message_dto.author),
            content=message_dto.content,
            timestamp=message_dto.timestamp
        )