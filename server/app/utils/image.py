from PIL import Image
import io
import base64

def prepare_image(image_bytes: bytes) -> str:
    """Resize, compress, and convert image bytes to base64 JPEG string."""
    img = Image.open(io.BytesIO(image_bytes))

    # Ensure no alpha channel
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Downscale to max 1024x1024 if needed using high-quality resampling
    img.thumbnail((1024, 1024), Image.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85, optimize=True)

    data = buffer.getvalue()

    return base64.b64encode(data).decode("utf-8") # Base64 string