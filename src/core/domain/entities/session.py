from dataclasses import dataclass
from typing import List
from uuid import uuid4
from core.domain.entities.message import Message
from domain.entities.user import User

@dataclass
class Session:
    id: str
    title: str
    messages: List[Message] = []
    
    @classmethod
    def create(cls, title: str, message: Message):
        return cls(
            id=str(uuid4()),
            title=title,
            messages=[message]
        )
    