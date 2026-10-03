def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
) -> list[dict]:
    chunks = []

    for page in pages:
        text = page["text"]

        for start in range(0, len(text), chunk_size):
            chunk_text = text[start:start + chunk_size]

            if chunk_text.strip():
                chunks.append(
                    {
                        "text": chunk_text,
                        "source": page["source"],
                        "page": page["page"],
                    }
                )

    return chunks