from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_embedding(description : str) -> list[float]:
    response = client.embeddings.create(
        input=description,
        model="text-embedding-3-small"
    )

    embedding_vector = response.data[0].embedding
    
    token_cost = embedding_vector.usage.total_tokens # will be used later for metrics and cost tracking
    return embedding_vector