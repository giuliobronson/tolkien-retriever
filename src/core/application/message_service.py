from typing import List
from core.domain.entities.message import Message
from core.application.ports.repositories.message_repository import IMessageRepository


class MessageService:
    def __init__(self, message_repository: IMessageRepository) -> None:
        self.message_repository = message_repository

    def get_message_history(self) -> List[Message]:
        return self.message_repository.get_all()

    def send_message(self, message: Message) -> Message:
        return self.message_repository.save(message)