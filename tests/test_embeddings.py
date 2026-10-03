from src.retrieval.embeddings import create_embeddings


def test_create_embeddings():
    embeddings = create_embeddings(
        ["Customer concentration is a key FDD risk."]
    )

    assert len(embeddings) == 1
    assert len(embeddings[0]) > 0