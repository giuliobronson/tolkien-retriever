from core.domain.entities.user import User
from core.ports.repositories.repository_port import RepositoryPort


class IUserRepository(RepositoryPort[User, str]):
    pass
