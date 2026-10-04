from src.agents.fdd_orchestrator import run_fdd_orchestrator
from src.agents.executive_summary_agent import create_executive_summary


def test_executive_summary_agent():
    result = run_fdd_orchestrator(
        "What are the key financial risks?"
    )

    summary = create_executive_summary(
        result["results"]
    )

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