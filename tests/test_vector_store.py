from src.retrieval.vector_store import create_vector_store


def test_vector_store():
    collection = create_vector_store()

    assert collection.name == "fdd_documents"