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

def test_fdd_finding_contains_provenance():
    result = analyze_fdd_question(
        "What is the main customer concentration risk?"
    )

    provenance = result["provenance"]

    assert provenance["question"] == (
        "What is the main customer concentration risk?"
    )
    assert provenance["agent"] == "FDD Analyzer"
    assert provenance["source"] == result["source"]
    assert provenance["page"] == result["page"]
    assert provenance["generated_at"]