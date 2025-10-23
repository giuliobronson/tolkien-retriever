from adapters.api.dto.author_dto import AuthorDTO
from core.domain.value_objects.author import Author


class AuthorMapper:
    @staticmethod
    def to_dto(author: Author) -> AuthorDTO:
        return AuthorDTO(name=author.role)

    @staticmethod
    def to_entity(author_dto: AuthorDTO) -> Author:
        return Author(role=author_dto.name)