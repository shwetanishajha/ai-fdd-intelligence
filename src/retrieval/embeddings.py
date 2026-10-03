from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def create_embeddings(
    texts: list[str],
    model: str = "text-embedding-3-small",
) -> list[list[float]]:
    client = OpenAI()

    response = client.embeddings.create(
        model=model,
        input=texts,
    )

    return [item.embedding for item in response.data]