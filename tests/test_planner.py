from unittest.mock import patch

import pytest

from src.agents.planner import create_fdd_plan


def test_planner_rejects_unsupported_agent():

    malicious_response = {
        "reasoning": "Attempt to select an unsupported agent",
        "selected_agents": ["Unsupported Agent"],
        "requires_executive_summary": False,
    }

    with patch(
        "src.agents.planner.call_llm"
    ) as mock_llm:

        mock_llm.return_value.choices = [
            type(
                "Choice",
                (),
                {
                    "message": type(
                        "Message",
                        (),
                        {
                            "content": (
                                '{"reasoning": "Attempt", '
                                '"selected_agents": ["Unsupported Agent"], '
                                '"requires_executive_summary": false}'
                            )
                        },
                    )()
                },
            )()
        ]

        with pytest.raises(ValueError):
            create_fdd_plan(
                "Analyze the financial risks"
            )