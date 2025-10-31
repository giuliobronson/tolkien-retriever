from dataclasses import dataclass, field
from typing import List
from uuid import uuid4
from core.domain.value_objects.message import Message


@dataclass
class Session:
    id: str
    title: str
    messages: List[Message] = field(default_factory=list)
    
    @classmethod
    def create(cls, title: str, message: Message):
        return cls(
            id=str(uuid4()),
            title=title,
            messages=[message]
        )
    