from pydantic import BaseModel


class UserDTO(BaseModel):
    name: str
    user_id: int