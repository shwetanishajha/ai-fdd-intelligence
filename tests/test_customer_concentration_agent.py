from src.agents.customer_concentration_agent import (
    analyze_customer_concentration,
)


def test_customer_concentration_agent():
    result = analyze_customer_concentration()

    assert result["agent"] == "Customer Concentration Agent"
    assert result["customer"] == "Customer A"
    assert result["revenue_percentage"] == 38.0
    assert result["risk_level"] == "High"
    assert len(result["evidence"]) > 0