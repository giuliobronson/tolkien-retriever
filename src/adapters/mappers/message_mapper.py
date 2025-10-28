from datetime import datetime
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

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
        kwargs = {"timestamp": message.timestamp or datetime.now()}
        if message.role == Role.USER:
            return HumanMessage(content=message.content, additional_kwargs=kwargs)
        elif message.role == Role.ASSISTANT:
            return AIMessage(content=message.content, additional_kwargs=kwargs)
        raise ValueError(f"Role desconhecida ao converter BaseMessage: {message.role}")
    
    @staticmethod
    def from_langgraph(message: BaseMessage) -> Message:
        return Message(
            role= MessageMapper._map_type_to_role(message.type),
            content=message.content,
            timestamp=message.additional_kwargs.get('timestamp')
        )
        
    @staticmethod
    def _map_type_to_role(type: str) -> Role:
        if type == "human":
            return Role.USER
        elif type == "ai":
            return Role.ASSISTANT
        raise ValueError(f"Tipo desconhecido ao converter Role: {type}")
