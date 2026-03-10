"""
Storage backend selection.

Centralizes storage backend configuration and instantiation based on
environment settings.
"""

import os
from pathlib import Path

from app.storage.storage_base import StorageBase
from app.storage.local_storage import LocalStorage
from app.core.config.config import settings
from app.storage.s3_storage import S3Storage


def get_storage_backend() -> StorageBase:
    """
    Return the configured storage backend.

    Defaults to local filesystem storage.
    """
    storage_type = settings.STORAGE_BACKEND
    # right now only local is an option, soon aws S3 will also be added.
    if storage_type == "local":
        return LocalStorage(
            base_dir=Path("/code/storage/images")
        )
    if storage_type == "s3":
        return S3Storage()


    raise ValueError(f"Unsupported storage_backend: {storage_type}")
