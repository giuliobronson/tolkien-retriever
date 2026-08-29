from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def stub_firebase_app(monkeypatch):
    """Unit tests never talk to Firebase.

    ``FirebaseAuthService.__init__`` calls ``firebase_admin.get_app()`` and, when
    no app exists, falls back to reading the credentials file pointed at by
    ``FIREBASE_CREDENTIALS_PATH`` — a path that only resolves on a developer
    machine with a real service-account JSON. Router tests that exercise the
    unauthenticated (401) path still trigger ``Depends(get_auth_service)``, so we
    make ``get_app()`` always return a stub and never hit the filesystem.
    """
    from infra.adapters.auth import firebase_auth_service

    monkeypatch.setattr(
        firebase_auth_service.firebase_admin,
        "get_app",
        lambda *args, **kwargs: MagicMock(),
    )
