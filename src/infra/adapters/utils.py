import hashlib
from pathlib import Path
from typing import Literal


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def calculate_file_hash(
    content: bytes, algorithm: Literal["sha256", "sha512"] = "sha256"
) -> str:
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(content)
    return hash_obj.hexdigest()
