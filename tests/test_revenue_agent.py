from src.agents.revenue_agent import analyze_revenue


def test_revenue_agent():
    result = analyze_revenue()

    assert result["agent"] == "Revenue Agent"
    assert result["previous_revenue"] == 47500000
    assert result["current_revenue"] == 54000000
    assert result["revenue_growth"] == 13.68
    assert result["risk_level"] == "Low"
    assert len(result["evidence"]) > 0