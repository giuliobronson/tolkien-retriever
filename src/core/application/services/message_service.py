from typing import List
from core.domain.entities.message import Message
from core.application.ports.repositories.message_repository import IMessageRepository


class MessageService:
    def __init__(self, message_repository: IMessageRepository) -> None:
        self.message_repository = message_repository
