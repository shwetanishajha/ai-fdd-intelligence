from src.agents.agentic_fdd import run_agentic_fdd


def test_agentic_fdd_end_to_end():
    result = run_agentic_fdd(
        "What are the key financial risks?"
    )

    assert result["plan"]["selected_agents"]
    assert len(result["results"]) >= 3

    assert result["executive_summary"] is not None

    summary = result["executive_summary"]

    assert "executive_summary" in summary
    assert "key_risks" in summary
    assert "further_diligence" in summary
    assert "overall_risk" in summary


def test_agentic_fdd_single_agent_question():
    result = run_agentic_fdd(
        "What was the FY2025 EBITDA margin?"
    )

    assert "EBITDA Agent" in result["plan"]["selected_agents"]
    assert len(result["results"]) >= 1