from src.retrieval.chunker import chunk_pages


def test_chunk_pages():
    pages = [
        {
            "text": "A" * 2500,
            "source": "financial_report.pdf",
            "page": 5,
        }
    ]

    chunks = chunk_pages(pages, chunk_size=1000)

    assert len(chunks) == 3
    assert chunks[0]["source"] == "financial_report.pdf"
    assert chunks[0]["page"] == 5