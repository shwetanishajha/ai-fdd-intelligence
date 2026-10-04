from src.agents.revenue_agent import analyze_revenue
from src.agents.ebitda_agent import analyze_ebitda
from src.agents.working_capital_agent import analyze_working_capital
from src.agents.customer_concentration_agent import (
    analyze_customer_concentration,
)
from src.agents.anomaly_agent import analyze_financial_anomalies


AGENT_REGISTRY = {
    "Revenue Agent": analyze_revenue,
    "EBITDA Agent": analyze_ebitda,
    "Working Capital Agent": analyze_working_capital,
    "Customer Concentration Agent": analyze_customer_concentration,
    "Financial Anomaly Agent": analyze_financial_anomalies,
}


def get_agent(agent_name: str):
    if agent_name not in AGENT_REGISTRY:
        raise ValueError(
            f"Unsupported agent: {agent_name}"
        )

    return AGENT_REGISTRY[agent_name]