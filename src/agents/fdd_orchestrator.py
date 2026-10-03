from src.agents.customer_concentration_agent import (
    analyze_customer_concentration,
)
from src.agents.ebitda_agent import analyze_ebitda


def run_fdd_orchestrator(question: str) -> dict:
    question_lower = question.lower()

    if any(
        keyword in question_lower
        for keyword in [
            "customer concentration",
            "customer dependency",
            "customer risk",
        ]
    ):
        return {
            "orchestrator": "FDD Orchestrator",
            "selected_agent": "Customer Concentration Agent",
            "result": analyze_customer_concentration(),
        }

    if any(
        keyword in question_lower
        for keyword in [
            "ebitda",
            "ebitda margin",
            "profitability",
        ]
    ):
        return {
            "orchestrator": "FDD Orchestrator",
            "selected_agent": "EBITDA Agent",
            "result": analyze_ebitda(),
        }

    return {
        "orchestrator": "FDD Orchestrator",
        "selected_agent": None,
        "result": None,
        "message": "No specialist agent currently supports this question.",
    }