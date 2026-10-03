import pandas as pd


def test_financial_data():
    df = pd.read_csv("data/financials/financials.csv")

    assert len(df) == 3
    assert df["revenue"].notna().all()
    assert df["ebitda"].notna().all()
    assert (df["ebitda"] > 0).all()