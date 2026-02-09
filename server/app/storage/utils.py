import os
import uuid


def generate_image_key(user_id: int, filename: str) -> str:
    """
    Generate a image identifier.
    """
    _, ext = os.path.splitext(filename)
    ext = ext.lower() or ".bin"

    return f"users/{user_id}/{uuid.uuid4().hex}{ext}"
