import datetime
from pydantic import BaseModel

from adapters.api.dto.author_dto import AuthorDTO


class MessageDTO(BaseModel):
    author: AuthorDTO
    content: str
    timestamp: datetime.datetime