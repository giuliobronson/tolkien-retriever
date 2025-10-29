import datetime
from pydantic import BaseModel
from core.domain.value_objects.role import Role


class MessageDTO(BaseModel):
    role: Role
    content: str
    timestamp: datetime.datetime