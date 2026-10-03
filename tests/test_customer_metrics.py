from src.validation.customer_metrics import calculate_customer_concentration


def test_customer_concentration():
    df = calculate_customer_concentration(
        "data/financials/customer_revenue.csv"
    )

    top_customer = df.iloc[0]

    assert top_customer["customer"] == "Customer A"
    assert round(top_customer["revenue_percentage"], 2) == 38.00