from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

from core.domain.value_objects.message import Message


@dataclass
class Session:
    id: str
    rulebook_id: str
    messages: List[Message] = field(default_factory=list)

    @classmethod
    def create(cls, rulebook_id: str):
        return cls(id=str(uuid4()), rulebook_id=rulebook_id)
