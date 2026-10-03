from src.retrieval.search import search_documents
from src.validation.customer_metrics import calculate_customer_concentration


def analyze_customer_concentration(
    customer_file: str = "data/financials/customer_revenue.csv",
) -> dict:
    evidence = search_documents(
        "What is the customer concentration risk?"
    )

    customer_data = calculate_customer_concentration(customer_file)

    top_customer = customer_data.iloc[0]

    return {
        "agent": "Customer Concentration Agent",
        "finding": (
            f"{top_customer['customer']} represents "
            f"{top_customer['revenue_percentage']:.0f}% "
            "of total FY2025 revenue."
        ),
        "risk_level": "High",
        "customer": top_customer["customer"],
        "revenue_percentage": round(
            top_customer["revenue_percentage"], 2
        ),
        "evidence": evidence,
    }