from src.ingestion.pdf_loader import load_pdf


def test_pdf_file_not_found():
    try:
        load_pdf("does-not-exist.pdf")
        assert False
    except FileNotFoundError:
        assert True