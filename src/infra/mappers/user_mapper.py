from typing import Optional

from core.domain.entities.user import User


class UserMapper:
    @staticmethod
    def to_document(user: User) -> dict:
        return {
            "uid": user.uid,
            "email": user.email,
            "email_verified": user.email_verified,
            "name": user.name,
        }

    @staticmethod
    def from_document(doc: Optional[dict]) -> Optional[User]:
        if not doc:
            return None
        return User(
            uid=doc["uid"],
            email=doc.get("email"),
            email_verified=doc.get("email_verified", False),
            name=doc.get("name"),
        )
