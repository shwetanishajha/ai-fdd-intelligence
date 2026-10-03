from src.ingestion.pdf_loader import load_pdf
from src.retrieval.chunker import chunk_pages
from src.retrieval.embeddings import create_embeddings
from src.retrieval.vector_store import create_vector_store


def index_pdf(file_path: str) -> int:
    pages = load_pdf(file_path)
    chunks = chunk_pages(pages)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = create_embeddings(texts)

    collection = create_vector_store()

    collection.upsert(
        ids=[f"{chunk['source']}-{chunk['page']}-{i}"
             for i, chunk in enumerate(chunks)],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "source": chunk["source"],
                "page": chunk["page"],
            }
            for chunk in chunks
        ],
    )

    return len(chunks)