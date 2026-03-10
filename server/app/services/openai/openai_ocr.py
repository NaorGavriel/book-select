from openai import OpenAI
import logging
from app.core.config.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
logger = logging.getLogger(settings.API_LOGGER_NAME)

def extract_books_spine_text(image_base64 : str) -> str:
    """Send bookshelf image to GPT-4o-mini and return extracted spine text as JSON."""
    instructions = (
        "You are performing visual OCR on a bookshelf image.\n\n"
        "Rules:\n"
        "- Each physical spine corresponds to one line of text.\n"
        "- Extract all visible text from each spine.\n"
        "- Combine vertically stacked text into a single line.\n"
        "- Do not separate title and author.\n"
        "- Do not interpret or identify the book.\n"
        "- Do not guess or use prior knowledge.\n"
        "- Return only the visible text.\n"
        "- Output JSON in this format:\n"
        "{ \"spines\": [\"text line\", ...] }"
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions= instructions,
        temperature=0,
        max_output_tokens=500,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Extract the text from each book spine. "
                        )
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                        "detail": "low"
                    },
                ],
            },
        ],
    )

    token_usage = response.usage

    usage_fields = {
        'input_tokens' : token_usage.input_tokens,
        'output_tokens' : token_usage.output_tokens,
        'total_tokens' : token_usage.total_tokens
    }
    
    logger.info("OPENAI OCR CALL", extra=usage_fields)
    return response.output_text # JSON string (not parsed)

