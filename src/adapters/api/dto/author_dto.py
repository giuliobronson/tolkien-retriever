from pydantic import BaseModel


class AuthorDTO(BaseModel):
    name: str