from core.domain.entities.rulebook import Rulebook
from core.ports.repositories.repository_port import RepositoryPort


class IRulebookRepository(RepositoryPort[Rulebook, str]):
    pass
