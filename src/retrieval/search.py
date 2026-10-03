from src.retrieval.embeddings import create_embeddings
from src.retrieval.vector_store import create_vector_store


def search_documents(
    query: str,
    top_k: int = 3,
    max_distance: float = 1.5,
) -> list[dict]:

    collection = create_vector_store()

    query_embedding = create_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    filtered_results = [
        (document, metadata, distance)
        for document, metadata, distance
        in zip(documents, metadatas, distances)
        if distance <= max_distance
    ]

    return [
        {
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": distance,
        }
        for document, metadata, distance in filtered_results
    ]