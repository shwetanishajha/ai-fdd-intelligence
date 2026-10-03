from src.agents.working_capital_agent import analyze_working_capital


def test_working_capital_agent():
    result = analyze_working_capital()

    assert result["agent"] == "Working Capital Agent"
    assert result["previous_working_capital"] == 6100000
    assert result["current_working_capital"] == 7200000
    assert result["change"] == 1100000
    assert result["risk_level"] == "Medium"
    assert len(result["evidence"]) > 0