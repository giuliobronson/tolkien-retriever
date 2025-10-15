import datetime
from pydantic import BaseModel

from core.application.services.dto.author_dto import AuthorDTO


class MessageDTO(BaseModel):
    author: AuthorDTO
    content: str
    timestamp: datetime.datetime