from core.application.ports.repositories.repository_port import RepositoryPort
from core.domain.entities.message import Message


class IMessageRepository(RepositoryPort[Message]):
    pass