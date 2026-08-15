from abc import ABC, abstractmethod

from core.domain.entities.authenticated_user import AuthenticatedUser


class IAuthService(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> AuthenticatedUser:
        """Valida o token e retorna o usuário autenticado."""
        pass
