from src.retrieval.search import search_documents
from src.validation.financial_metrics import calculate_metrics


def analyze_working_capital(
    financial_file: str = "data/financials/financials.csv",
) -> dict:
    evidence = search_documents(
        "How did working capital change?"
    )

    financial_data = calculate_metrics(financial_file)

    previous = financial_data.iloc[-2]
    latest = financial_data.iloc[-1]

    change = latest["working_capital"] - previous["working_capital"]

    return {
        "agent": "Working Capital Agent",
        "finding": (
            f"Working capital increased from "
            f"£{previous['working_capital'] / 1_000_000:.1f} million "
            f"to £{latest['working_capital'] / 1_000_000:.1f} million, "
            f"an increase of £{change / 1_000_000:.1f} million."
        ),
        "risk_level": "Medium",
        "previous_working_capital": previous["working_capital"],
        "current_working_capital": latest["working_capital"],
        "change": change,
        "evidence": evidence,
    }