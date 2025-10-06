from typing import List
from application.use_cases.dto.message_dto import MessageDTO
from application.use_cases.dto.user_dto import UserDTO
from pydantic import BaseModel


class Session(BaseModel):
    user: UserDTO
    title: str
    messages = List[MessageDTO]