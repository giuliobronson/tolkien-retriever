import asyncio
from typing import Dict

import firebase_admin
from firebase_admin import auth, credentials

from core.domain.entities.user import User
from core.domain.exceptions.expired_token_error import ExpiredTokenError
from core.domain.exceptions.invalid_token_error import InvalidTokenError
from core.domain.exceptions.revoked_token_error import RevokedTokenError
from core.ports.auth.auth_service import IAuthService


class FirebaseAuthService(IAuthService):
    def __init__(self, credentials_path: str):
        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(credentials_path)
            self.app = firebase_admin.initialize_app(cred)

    async def verify_token(self, token: str) -> User:
        try:
            decoded: Dict = await asyncio.to_thread(
                auth.verify_id_token, token, app=self.app, check_revoked=True
            )
        except auth.ExpiredIdTokenError as e:
            raise ExpiredTokenError("Token expirado") from e
        except auth.RevokedIdTokenError as e:
            raise RevokedTokenError("Token revogado") from e
        except auth.InvalidIdTokenError as e:
            raise InvalidTokenError("Token inválido") from e
        except auth.CertificateFetchError as e:
            raise InvalidTokenError("Não foi possível verificar o token") from e

        return User(
            uid=decoded["uid"],
            email=decoded.get("email"),
            email_verified=decoded.get("email_verified", False),
            name=decoded.get("name"),
        )

    async def delete_user(self, uid: str) -> None:
        try:
            await asyncio.to_thread(auth.delete_user, uid, app=self.app)
        except auth.UserNotFoundError:
            pass
