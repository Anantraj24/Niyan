import hashlib
from pathlib import Path

def compute_sha256_bytes(data: bytes) -> str:
    """Compute SHA256 hex digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()

def compute_sha256_file(file_path: Path | str) -> str:
    """Compute SHA256 hex digest of a file in chunks."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()
