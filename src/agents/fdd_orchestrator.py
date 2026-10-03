from src.agents.customer_concentration_agent import (
    analyze_customer_concentration,
)
from src.agents.ebitda_agent import analyze_ebitda
from src.agents.working_capital_agent import analyze_working_capital


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

    if any(
        keyword in question_lower
        for keyword in [
            "working capital",
            "working-capital",
            "cash conversion",
        ]
    ):
        return {
            "orchestrator": "FDD Orchestrator",
            "selected_agent": "Working Capital Agent",
            "result": analyze_working_capital(),
        }

    return {
        "orchestrator": "FDD Orchestrator",
        "selected_agent": None,
        "result": None,
        "message": "No specialist agent currently supports this question.",
    }