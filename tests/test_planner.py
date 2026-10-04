from src.agents.planner import create_fdd_plan
import pytest
from unittest.mock import patch

def test_planner_rejects_unsupported_agent():
    fake_response = type(
        "FakeResponse",
        (),
        {
            "choices": [
                type(
                    "FakeChoice",
                    (),
                    {
                        "message": type(
                            "FakeMessage",
                            (),
                            {
                                "content": (
                                    '{"reasoning": "Test", '
                                    '"selected_agents": ["Malicious Agent"], '
                                    '"requires_executive_summary": false}'
                                )
                            },
                        )()
                    },
                )()
            ]
        },
    )()

    with patch(
        "src.agents.planner.client.chat.completions.create",
        return_value=fake_response,
    ):
        with pytest.raises(ValueError, match="unsupported agents"):
            create_fdd_plan("Assess the company.")


def test_fdd_planner_selects_customer_agent():
    plan = create_fdd_plan(
        "What is the customer concentration risk?"
    )

    assert "Customer Concentration Agent" in plan["selected_agents"]


def test_fdd_planner_selects_multiple_agents():
    plan = create_fdd_plan(
        "What are the key financial risks?"
    )

    assert len(plan["selected_agents"]) >= 3
    assert plan["requires_executive_summary"] is True

def test_planner_only_allows_supported_agents():
    plan = create_fdd_plan(
        "Assess revenue, EBITDA and customer concentration risks."
    )

    allowed_agents = {
        "Revenue Agent",
        "EBITDA Agent",
        "Working Capital Agent",
        "Customer Concentration Agent",
        "Financial Anomaly Agent",
    }

    assert set(plan["selected_agents"]).issubset(allowed_agents)