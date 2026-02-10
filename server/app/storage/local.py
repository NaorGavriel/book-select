from pathlib import Path
from app.storage.utils import generate_image_key
from app.storage.storage_base import StorageBase


class LocalStorage(StorageBase):
    """
    Store images on the local filesystem.
    """
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def save_image(self, *, image_bytes: bytes, filename: str, user_id: int) -> str:
        """
        Persist image bytes locally and return the storage key.
        """
        key = generate_image_key(user_id=user_id, filename=filename)

        # image_path is storage backend-specific
        image_path = self.base_dir / key
        image_path.parent.mkdir(parents=True, exist_ok=True)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        return key
    
    def load_image(self, key: str) -> bytes:
        '''        
        Load an image from local storage.
        '''
        image_path = self.base_dir / key

        with open(image_path, "rb") as f:
            return f.read()
