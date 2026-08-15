from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthenticatedUser:
    uid: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
