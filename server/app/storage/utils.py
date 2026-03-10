import os
import uuid

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

def generate_image_key(user_id: int, extension : str) -> str:
    """
    Generate a unique image key for a user.
    Images are stored as JPEG.
    """
    extension = extension.lower().lstrip(".")
    
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported image format")
    
    return f"users/{user_id}/{uuid.uuid4().hex}.{extension}"
