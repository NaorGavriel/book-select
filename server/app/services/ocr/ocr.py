from app.services.openai.openai_ocr import extract_books_spine_text
from app.utils.image import prepare_image
import json

def extract_books_from_image(image_bytes: bytes) -> list[str]:
    """Process image bytes, run OCR, and return extracted spine text list."""

    prepared_image = prepare_image(image_bytes=image_bytes)
    output_text = extract_books_spine_text(prepared_image)

    try:
        output_dict = json.loads(output_text)
        return output_dict.get("spines", []) # Extract spine list from JSON response
    except json.JSONDecodeError:
        print("json decode error")
        return []
