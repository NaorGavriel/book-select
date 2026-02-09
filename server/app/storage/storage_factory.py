"""
Storage backend selection.

Centralizes storage backend configuration and instantiation based on
environment settings.
"""

import os
from pathlib import Path

from app.storage.storage_base import StorageBase
from app.storage.local import LocalStorage

def get_storage_backend() -> StorageBase:
    """
    Return the configured storage backend.

    Defaults to local filesystem storage.
    """
    backend = os.getenv("STORAGE_BACKEND", "local")

    # right now only local is an option, soon aws S3 will also be added.
    if backend == "local":
        return LocalStorage(
            base_dir=Path("/code/storage/images")
        )

    raise ValueError(f"Unsupported storage_backend: {backend}")
