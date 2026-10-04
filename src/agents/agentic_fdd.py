from src.agents.planner import create_fdd_plan
from src.agents.executor import execute_plan
from src.agents.executive_summary_agent import create_executive_summary


def run_agentic_fdd(question: str) -> dict:
    plan = create_fdd_plan(question)

    specialist_results = execute_plan(
        plan["selected_agents"]
    )

    executive_summary = None

    if plan["requires_executive_summary"]:
        executive_summary = create_executive_summary(
            specialist_results
        )

    return {
        "question": question,
        "plan": plan,
        "results": specialist_results,
        "executive_summary": executive_summary,
    }