import hashlib
from typing import Literal


def calculate_file_hash(
    content: bytes, algorithm: Literal["sha256", "sha512"] = "sha256"
) -> str:
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(content)
    return hash_obj.hexdigest()
