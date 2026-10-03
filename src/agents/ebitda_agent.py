from src.retrieval.search import search_documents
from src.validation.financial_metrics import calculate_metrics


def analyze_ebitda(
    financial_file: str = "data/financials/financials.csv",
) -> dict:
    evidence = search_documents(
        "What was the FY2025 EBITDA margin?"
    )

    financial_data = calculate_metrics(financial_file)

    latest = financial_data.iloc[-1]

    return {
        "agent": "EBITDA Agent",
        "finding": (
            f"FY2025 EBITDA was £{latest['ebitda'] / 1_000_000:.2f} million "
            f"with an EBITDA margin of "
            f"{latest['ebitda_margin']:.1f}%."
        ),
        "risk_level": "Medium",
        "ebitda": latest["ebitda"],
        "ebitda_margin": round(latest["ebitda_margin"], 2),
        "evidence": evidence,
    }