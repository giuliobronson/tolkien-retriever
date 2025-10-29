from core.domain.entities.session import Session
from core.ports.repositories.repository_port import RepositoryPort


class ISessionRepository(RepositoryPort[Session, str]):
    pass