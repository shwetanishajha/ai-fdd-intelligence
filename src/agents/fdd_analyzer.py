import json
from datetime import datetime, timezone

from dotenv import load_dotenv

from src.retrieval.search import search_documents
from src.agents.models import FDDFinding
from src.core.llm_client import call_llm

load_dotenv()


def analyze_fdd_question(question: str) -> dict:
    evidence = search_documents(question)

    evidence_text = "\n\n".join(
        f"Source: {item['source']}, Page: {item['page']}\n{item['text']}"
        for item in evidence
    )

    prompt = f"""
You are a financial due diligence analyst.

Answer the user's question using ONLY the evidence provided below.

Question:
{question}

Evidence:
{evidence_text}

Return valid JSON with exactly these fields:
- finding
- risk_level
- evidence
- source
- page
- confidence

Confidence:
Return a number between 0 and 1.

Do not invent facts that are not supported by the evidence.
"""

    response = call_llm(
        messages=[
            {
                "role": "system",
                "content": (
                    "You produce evidence-backed financial "
                    "due diligence findings."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
    )

    finding = FDDFinding.model_validate(
        json.loads(response.choices[0].message.content)
    )

    finding.provenance = {
        "question": question,
        "agent": "FDD Analyzer",
        "source": finding.source,
        "page": finding.page,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    return finding.model_dump()