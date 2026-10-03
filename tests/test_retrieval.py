from src.retrieval.search import search_documents


def test_customer_concentration_retrieval():
    results = search_documents(
        "What is the customer concentration risk?"
    )

    assert len(results) > 0
    assert any(
        "Customer A" in result["text"]
        for result in results
    )
    assert any(
        result["source"] == "fdd_report.pdf"
        for result in results
    )