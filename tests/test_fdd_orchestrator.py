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

def test_revenue_routing():
    result = run_fdd_orchestrator(
        "How did revenue change?"
    )

    assert result["orchestrator"] == "FDD Orchestrator"
    assert result["selected_agent"] == "Revenue Agent"
    assert result["result"]["revenue_growth"] == 13.68
    assert result["result"]["risk_level"] == "Low"

def test_financial_anomaly_routing():
    result = run_fdd_orchestrator(
        "What financial anomalies require further diligence?"
    )

    assert result["orchestrator"] == "FDD Orchestrator"
    assert result["selected_agent"] == "Financial Anomaly Agent"
    assert result["result"]["risk_level"] == "Medium"
    assert len(result["result"]["finding"]) > 0

def test_multi_agent_fdd_analysis():
    result = run_fdd_orchestrator(
        "What are the key financial risks?"
    )

    expected_agents = {
        "Revenue Agent",
        "EBITDA Agent",
        "Working Capital Agent",
        "Customer Concentration Agent",
        "Financial Anomaly Agent",
    }

    assert result["orchestrator"] == "FDD Orchestrator"
    assert set(result["selected_agents"]) == expected_agents
    assert len(result["results"]) == 5