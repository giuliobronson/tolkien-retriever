from typing import Literal
from langchain_core.messages import BaseMessage
from langchain.messages import AIMessage, HumanMessage

from adapters.api.dto.message_dto import MessageDTO
from core.domain.value_objects.message import Message
from core.domain.value_objects.role import Role


class MessageMapper:
    @staticmethod
    def to_dto(message: Message) -> MessageDTO:
        return MessageDTO(
            role=message.role,
            content=message.content,
            timestamp=message.timestamp
        )

    @staticmethod
    def to_entity(message_dto: MessageDTO):
        return Message(
            role=message_dto.role,
            content=message_dto.content,
            timestamp=message_dto.timestamp
        )
        
    @staticmethod
    def to_langgraph(message: Message) -> BaseMessage:
        if message.role == Role.USER:
            return HumanMessage(content=message.content)
        elif message.role == Role.ASSISTENT:
            return AIMessage(content=message.content)
        raise ValueError(f"Role desconhecida ao converter BaseMessage: {message.role}")
    
    @staticmethod
    def from_langgraph(message: BaseMessage) -> Message:
        return Message(
            role=Role(message.type),
            content=message.content,
            timestamp=message.additional_kwargs.get('timestamp')
        )
        
    @staticmethod
    def map_content(content: str | list[str | dict]) -> str:
        