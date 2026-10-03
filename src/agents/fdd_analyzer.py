import json


from dotenv import load_dotenv
from openai import OpenAI
from src.agents.models import FDDFinding

from src.retrieval.search import search_documents

load_dotenv()

client = OpenAI()


def analyze_fdd_question(question: str) -> dict:
    evidence = search_documents(question)

    evidence_text = "\n\n".join(
        f"Source: {item['source']}, Page: {item['page']}\n"
        f"{item['text']}"
        for item in evidence
    )

    prompt = f"""
You are a financial due diligence analyst.

Answer the user's question using ONLY the evidence provided below.

Question:
{question}

Evidence:
{evidence_text}

confidence:
Return a number between 0 and 1.

Return valid JSON with exactly these fields:
- finding
- risk_level
- evidence
- source
- page
- confidence

Do not invent facts that are not supported by the evidence.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You produce evidence-backed financial due diligence findings.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return FDDFinding.model_validate(
    json.loads(response.choices[0].message.content)
).model_dump()