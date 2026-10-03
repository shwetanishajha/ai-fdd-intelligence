import chromadb


def create_vector_store():
    client = chromadb.PersistentClient(
        path="data/chroma"
    )

    collection = client.get_or_create_collection(
        name="fdd_documents"
    )

    return collection