from openai import OpenAI
from app.core.config import APIsConfig

client = OpenAI(api_key=APIsConfig.OPENAI_API_KEY)

def generate_embedding(description : str) -> list[float]:
    """
    Generate a vector embedding for a given text description using OpenAI embedding model.

    Args:
        description (str): Text to embed.

    Returns:
        list[float]: Embedding vector representing the input text.
    """
    response = client.embeddings.create(
        input=description,
        model="text-embedding-3-small"
    )

    embedding_vector = response.data[0].embedding # Extract embedding vector from response
    
    token_cost = response.usage.total_tokens # will be used later for metrics and cost tracking
    return embedding_vector