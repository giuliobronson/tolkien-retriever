from typing import List

from pydantic import BaseModel

from infra.drivers.api.dto.message_dto import MessageDTO


class SessionDTO(BaseModel):
    id: str
    rulebook_id: str
    messages: List[MessageDTO]
