from app.services.openai.openai_ocr import extract_books_spine_text
import json
import base64

def extract_books_from_image(image_bytes: bytes) -> list[str]:
    """Process image bytes, run OCR, and return extracted spine text list."""

    converted_image = base64.b64encode(image_bytes).decode("utf-8") # converting the image from bytes to str in base64
    output_text = extract_books_spine_text(converted_image)

    try:
        output_dict = json.loads(output_text)
        return output_dict.get("spines", []) # Extract spine list from JSON response
    except json.JSONDecodeError:
        print("json decode error")
        return []
