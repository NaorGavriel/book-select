from PIL import Image, ImageOps
from io import BytesIO

def process_image(image_bytes: bytes) -> bytes:
    with Image.open(BytesIO(image_bytes)) as original_img:
        img = ImageOps.exif_transpose(original_img)
        img = ImageOps.fit(img, (1024,1024), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85, optimize=True)

        data = buffer.getvalue()

    return data