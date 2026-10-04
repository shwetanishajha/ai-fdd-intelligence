from src.agents.fdd_orchestrator import run_fdd_orchestrator


def test_fdd_end_to_end():
    result = run_fdd_orchestrator(
        "What are the key financial risks?"
    )

    assert result["orchestrator"] == "FDD Orchestrator"

    assert len(result["selected_agents"]) == 5
    assert len(result["results"]) == 5

    assert "executive_summary" in result

    summary = result["executive_summary"]

    assert "executive_summary" in summary
    assert "key_risks" in summary
    assert "further_diligence" in summary
    assert "overall_risk" in summary

    assert summary["overall_risk"] in {
        "Low",
        "Medium",
        "Medium to High",
        "High",
    }

    assert len(summary["key_risks"]) > 0
    assert len(summary["further_diligence"]) > 0