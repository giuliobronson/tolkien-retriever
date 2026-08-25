from abc import ABC, abstractmethod

from core.domain.entities.user import User


class IAuthService(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> User:
        """Valida o token e retorna o usuário autenticado."""
        pass

    @abstractmethod
    async def delete_user(self, uid: str) -> None:
        """Exclui o usuário no provedor de autenticação."""
        pass
