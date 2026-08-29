from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def stub_firebase_app(monkeypatch):
    from infra.adapters.auth import firebase_auth_service

    monkeypatch.setattr(
        firebase_auth_service.firebase_admin,
        "get_app",
        lambda *args, **kwargs: MagicMock(),
    )
