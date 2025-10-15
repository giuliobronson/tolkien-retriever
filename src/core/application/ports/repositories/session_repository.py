from core.application.ports.repositories.repository_port import RepositoryPort
from core.domain.entities.session import Session


class ISessionRepository(RepositoryPort[Session]):
    pass