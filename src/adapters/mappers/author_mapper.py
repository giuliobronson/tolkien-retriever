from adapters.api.dto.author_dto import AuthorDTO
from core.domain.entities.author import Author


class AuthorMapper:
    @staticmethod
    def to_dto(author: Author) -> AuthorDTO:
        return AuthorDTO(name=author.name)

    @staticmethod
    def to_entity(author_dto: AuthorDTO) -> Author:
        return Author(name=author_dto.name)