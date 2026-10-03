from src.agents.ebitda_agent import analyze_ebitda


def test_ebitda_agent():
    result = analyze_ebitda()

    assert result["agent"] == "EBITDA Agent"
    assert result["ebitda_margin"] == 17.0
    assert result["risk_level"] == "Medium"
    assert len(result["evidence"]) > 0