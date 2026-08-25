# Feature module: only imports leaf modules (repositories/storage/pipeline/agents) — never another feature module in dependencies/.
from functools import lru_cache

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import FIREBASE_CREDENTIALS_PATH
from core.application.services.user_service import UserService
from core.domain.entities.user import User
from core.domain.exceptions.missing_token_error import MissingTokenError
from core.ports.auth.auth_service import IAuthService
from core.ports.repositories.user_repository import IUserRepository
from infra.adapters.auth.firebase_auth_service import FirebaseAuthService
from infra.drivers.api.dependencies.repositories import get_user_repository

bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache
def get_auth_service() -> IAuthService:
    return FirebaseAuthService(credentials_path=FIREBASE_CREDENTIALS_PATH)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: IAuthService = Depends(get_auth_service),
) -> User:
    if credentials is None:
        raise MissingTokenError("Token de autenticação não informado")
    return await auth_service.verify_token(credentials.credentials)


async def get_user_service(
    repository: IUserRepository = Depends(get_user_repository),
    auth_service: IAuthService = Depends(get_auth_service),
):
    service = UserService(repository, auth_service)
    yield service


async def get_authenticated_user(
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> User:
    return await user_service.get_or_create_user(user)
