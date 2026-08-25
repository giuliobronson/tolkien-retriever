from unittest.mock import MagicMock, patch

import pytest
from firebase_admin import auth as firebase_auth

from core.domain.exceptions.expired_token_error import ExpiredTokenError
from core.domain.exceptions.invalid_token_error import InvalidTokenError
from core.domain.exceptions.revoked_token_error import RevokedTokenError
from infra.adapters.auth.firebase_auth_service import FirebaseAuthService


class TestFirebaseAuthService:

    @pytest.fixture
    def service(self) -> FirebaseAuthService:
        with patch(
            "infra.adapters.auth.firebase_auth_service.firebase_admin.get_app"
        ) as mock_get_app:
            mock_get_app.return_value = MagicMock()
            return FirebaseAuthService(credentials_path="unused.json")

    @pytest.mark.asyncio
    async def test_verify_token_returns_authenticated_user(
        self, service: FirebaseAuthService
    ) -> None:
        decoded = {
            "uid": "abc123",
            "email": "frodo@shire.com",
            "email_verified": True,
            "name": "Frodo Baggins",
        }

        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.verify_id_token",
            return_value=decoded,
        ) as mock_verify:
            result = await service.verify_token("valid-token")

        mock_verify.assert_called_once_with(
            "valid-token", app=service.app, check_revoked=True
        )
        assert result.uid == "abc123"
        assert result.email == "frodo@shire.com"
        assert result.email_verified is True
        assert result.name == "Frodo Baggins"

    @pytest.mark.asyncio
    async def test_verify_token_missing_optional_claims_uses_defaults(
        self, service: FirebaseAuthService
    ) -> None:
        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.verify_id_token",
            return_value={"uid": "abc123"},
        ):
            result = await service.verify_token("valid-token")

        assert result.uid == "abc123"
        assert result.email is None
        assert result.email_verified is False
        assert result.name is None

    @pytest.mark.asyncio
    async def test_verify_token_expired_raises_expired_token_error(
        self, service: FirebaseAuthService
    ) -> None:
        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.verify_id_token",
            side_effect=firebase_auth.ExpiredIdTokenError("expired", cause=None),
        ):
            with pytest.raises(ExpiredTokenError):
                await service.verify_token("expired-token")

    @pytest.mark.asyncio
    async def test_verify_token_revoked_raises_revoked_token_error(
        self, service: FirebaseAuthService
    ) -> None:
        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.verify_id_token",
            side_effect=firebase_auth.RevokedIdTokenError("revoked"),
        ):
            with pytest.raises(RevokedTokenError):
                await service.verify_token("revoked-token")

    @pytest.mark.asyncio
    async def test_verify_token_invalid_raises_invalid_token_error(
        self, service: FirebaseAuthService
    ) -> None:
        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.verify_id_token",
            side_effect=firebase_auth.InvalidIdTokenError("invalid"),
        ):
            with pytest.raises(InvalidTokenError):
                await service.verify_token("invalid-token")

    @pytest.mark.asyncio
    async def test_verify_token_certificate_fetch_error_raises_invalid_token_error(
        self, service: FirebaseAuthService
    ) -> None:
        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.verify_id_token",
            side_effect=firebase_auth.CertificateFetchError("cert error", cause=None),
        ):
            with pytest.raises(InvalidTokenError):
                await service.verify_token("token")

    @pytest.mark.asyncio
    async def test_delete_user_calls_firebase_delete_user(
        self, service: FirebaseAuthService
    ) -> None:
        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.delete_user"
        ) as mock_delete:
            await service.delete_user("abc123")

        mock_delete.assert_called_once_with("abc123", app=service.app)

    @pytest.mark.asyncio
    async def test_delete_user_ignores_unknown_firebase_user(
        self, service: FirebaseAuthService
    ) -> None:
        with patch(
            "infra.adapters.auth.firebase_auth_service.auth.delete_user",
            side_effect=firebase_auth.UserNotFoundError("not found"),
        ):
            await service.delete_user("abc123")
