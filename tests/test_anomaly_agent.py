from src.agents.anomaly_agent import analyze_financial_anomalies


def test_financial_anomaly_agent():
    result = analyze_financial_anomalies()

    assert result["agent"] == "Financial Anomaly Agent"
    assert result["risk_level"] == "Medium"

    assert any(
        "Working capital increased by more than £1 million"
        in finding
        for finding in result["finding"]
    )

    assert any(
        "Revenue grew by 13.7%"
        in finding
        for finding in result["finding"]
    )

    assert any(
        "EBITDA margin was 17.0%"
        in finding
        for finding in result["finding"]
    )

    assert len(result["evidence"]) > 0