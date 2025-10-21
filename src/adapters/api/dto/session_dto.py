from typing import List
from pydantic import BaseModel

from adapters.api.dto.message_dto import MessageDTO
from adapters.api.dto.user_dto import UserDTO


class SessionDTO(BaseModel):
    id: str
    title: str
    messages: List[MessageDTO]