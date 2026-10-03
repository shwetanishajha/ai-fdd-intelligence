from src.retrieval.embeddings import create_embeddings
from src.retrieval.vector_store import create_vector_store


def search_documents(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    collection = create_vector_store()

    query_embedding = create_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return [
        {
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
        }
        for document, metadata in zip(documents, metadatas)
    ]