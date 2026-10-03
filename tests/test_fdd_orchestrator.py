from src.agents.fdd_orchestrator import run_fdd_orchestrator


def test_customer_concentration_routing():
    result = run_fdd_orchestrator(
        "What is the customer concentration risk?"
    )

    assert result["orchestrator"] == "FDD Orchestrator"
    assert result["selected_agent"] == "Customer Concentration Agent"
    assert result["result"]["customer"] == "Customer A"
    assert result["result"]["risk_level"] == "High"


def test_unsupported_question():
    result = run_fdd_orchestrator(
        "What is the employee satisfaction score?"
    )

    assert result["selected_agent"] is None
    assert result["result"] is None

def test_working_capital_routing():
    result = run_fdd_orchestrator(
        "How did working capital change?"
    )

    assert result["orchestrator"] == "FDD Orchestrator"
    assert result["selected_agent"] == "Working Capital Agent"
    assert result["result"]["change"] == 1100000
    assert result["result"]["risk_level"] == "Medium"