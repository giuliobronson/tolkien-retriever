from functools import lru_cache

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import FIREBASE_CREDENTIALS_PATH
from core.domain.entities.authenticated_user import AuthenticatedUser
from core.domain.exceptions.missing_token_error import MissingTokenError
from core.ports.auth.auth_service import IAuthService
from infra.adapters.auth.firebase_auth_service import FirebaseAuthService

bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache
def get_auth_service() -> IAuthService:
    return FirebaseAuthService(credentials_path=FIREBASE_CREDENTIALS_PATH)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: IAuthService = Depends(get_auth_service),
) -> AuthenticatedUser:
    if credentials is None:
        raise MissingTokenError("Token de autenticação não informado")
    return await auth_service.verify_token(credentials.credentials)
