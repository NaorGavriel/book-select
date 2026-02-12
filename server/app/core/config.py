import os
from dotenv import load_dotenv

load_dotenv()


# OCR api
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google api settings
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
MAX_RESULTS = os.getenv("GOOGLE_BOOKS_MAX_RESULTS")

# Settings : 
BOOK_CACHE_THRESHOLD = float(os.getenv("BOOK_CACHE_THRESHOLD"))