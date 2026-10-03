import pandas as pd


def calculate_metrics(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["revenue_growth"] = df["revenue"].pct_change() * 100
    df["ebitda_margin"] = (df["ebitda"] / df["revenue"]) * 100

    return df