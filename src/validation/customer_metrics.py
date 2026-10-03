import pandas as pd


def calculate_customer_concentration(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    total_revenue = df["2025_revenue"].sum()

    df["revenue_percentage"] = (
        df["2025_revenue"] / total_revenue
    ) * 100

    return df.sort_values(
        "revenue_percentage",
        ascending=False,
    )