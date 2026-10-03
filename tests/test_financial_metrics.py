from src.validation.financial_metrics import calculate_metrics


def test_financial_metrics():
    df = calculate_metrics("data/financials/financials.csv")

    assert round(df.iloc[1]["revenue_growth"], 2) == 13.10
    assert round(df.iloc[2]["ebitda_margin"], 2) == 17.00