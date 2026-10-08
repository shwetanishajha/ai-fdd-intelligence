from src.agents.agentic_fdd import run_agentic_fdd
from src.agents.customer_concentration_agent import analyze_customer_concentration
from src.agents.ebitda_agent import analyze_ebitda
from src.agents.working_capital_agent import analyze_working_capital
from src.agents.revenue_agent import analyze_revenue
from src.agents.anomaly_agent import analyze_financial_anomalies
from src.agents.report_agent import create_fdd_report
from src.reporting.report_generator import generate_fdd_pdf


def run_fdd(mode: str, question: str | None = None) -> dict:
    if mode == "query":
        if not question:
            raise ValueError("question is required for query mode")

        return run_agentic_fdd(question)

    if mode == "generate":
        results = [
            analyze_revenue(),
            analyze_ebitda(),
            analyze_working_capital(),
            analyze_customer_concentration(),
            analyze_financial_anomalies(),
        ]

        report = create_fdd_report(results)

        pdf_path = generate_fdd_pdf(
            report,
            "data/fdd_report_generated.pdf",
        )

        return {
            "mode": "generate",
            "execution": {
                "agent_count": len(results),
                "agents_executed": [
                    result["agent"] for result in results
                ],
            },
            "report": report,
            "pdf_path": pdf_path,
        }

    raise ValueError("mode must be 'generate' or 'query'")