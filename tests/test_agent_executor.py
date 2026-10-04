import pytest

from src.agents.executor import execute_plan


def test_executor_runs_selected_agents():
    results = execute_plan(
        [
            "Revenue Agent",
            "EBITDA Agent",
        ]
    )

    assert len(results) == 2
    assert results[0]["agent"] == "Revenue Agent"
    assert results[1]["agent"] == "EBITDA Agent"


def test_executor_rejects_unsupported_agent():
    with pytest.raises(
        ValueError,
        match="Unsupported agent",
    ):
        execute_plan(
            [
                "Revenue Agent",
                "Malicious Agent",
            ]
        )