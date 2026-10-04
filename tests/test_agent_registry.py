import pytest

from src.agents.registry import get_agent


def test_registry_returns_revenue_agent():
    agent = get_agent("Revenue Agent")

    assert callable(agent)
    assert agent.__name__ == "analyze_revenue"


def test_registry_returns_ebitda_agent():
    agent = get_agent("EBITDA Agent")

    assert callable(agent)
    assert agent.__name__ == "analyze_ebitda"


def test_registry_rejects_unsupported_agent():
    with pytest.raises(
        ValueError,
        match="Unsupported agent",
    ):
        get_agent("Malicious Agent")