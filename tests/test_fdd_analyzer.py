from src.agents.fdd_analyzer import analyze_fdd_question


def test_fdd_analyzer():
    result = analyze_fdd_question(
        "What is the main customer concentration risk?"
    )

    assert result["finding"]
    assert result["risk_level"] in ["Low", "Medium", "High"]
    assert result["evidence"]
    assert result["source"] == "fdd_report.pdf"
    assert result["page"] == 1