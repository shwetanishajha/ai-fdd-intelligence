from src.retrieval.search import search_documents
from src.validation.financial_metrics import calculate_metrics


def analyze_revenue(
    financial_file: str = "data/financials/financials.csv",
) -> dict:
    evidence = search_documents(
        "How did revenue change from FY2024 to FY2025?"
    )

    financial_data = calculate_metrics(financial_file)

    previous = financial_data.iloc[-2]
    latest = financial_data.iloc[-1]

    growth = latest["revenue_growth"]

    return {
        "agent": "Revenue Agent",
        "finding": (
            f"Revenue increased from "
            f"£{previous['revenue'] / 1_000_000:.1f} million "
            f"to £{latest['revenue'] / 1_000_000:.1f} million, "
            f"representing {growth:.1f}% growth."
        ),
        "risk_level": "Low",
        "previous_revenue": previous["revenue"],
        "current_revenue": latest["revenue"],
        "revenue_growth": round(growth, 2),
        "evidence": evidence,
    }