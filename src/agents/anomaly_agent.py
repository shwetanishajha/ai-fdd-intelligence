from src.retrieval.search import search_documents
from src.validation.financial_metrics import calculate_metrics


def analyze_financial_anomalies(
    financial_file: str = "data/financials/financials.csv",
) -> dict:
    evidence = search_documents(
        "What financial anomalies or unusual movements require further diligence?"
    )

    financial_data = calculate_metrics(financial_file)

    previous = financial_data.iloc[-2]
    latest = financial_data.iloc[-1]

    revenue_growth = latest["revenue_growth"]
    ebitda_margin = latest["ebitda_margin"]

    working_capital_change = (
        latest["working_capital"] - previous["working_capital"]
    )

    findings = []

    if working_capital_change > 1_000_000:
        findings.append(
            "Working capital increased by more than £1 million."
        )

    if revenue_growth > 10:
        findings.append(
            f"Revenue grew by {revenue_growth:.1f}% year-on-year."
        )

    if ebitda_margin < 20:
        findings.append(
            f"EBITDA margin was {ebitda_margin:.1f}%."
        )

    return {
        "agent": "Financial Anomaly Agent",
        "finding": findings,
        "risk_level": "Medium",
        "evidence": evidence,
    }