from src.agents.planner import create_fdd_plan


def test_planner_revenue_question():
    plan = create_fdd_plan(
        "How did revenue change from FY2024 to FY2025?"
    )

    assert "Revenue Agent" in plan["selected_agents"]


def test_planner_ebitda_question():
    plan = create_fdd_plan(
        "What was the FY2025 EBITDA margin?"
    )

    assert "EBITDA Agent" in plan["selected_agents"]


def test_planner_working_capital_question():
    plan = create_fdd_plan(
        "How did working capital change?"
    )

    assert "Working Capital Agent" in plan["selected_agents"]


def test_planner_overall_fdd_question():
    plan = create_fdd_plan(
        "Give me an overall FDD assessment and key financial risks."
    )

    assert len(plan["selected_agents"]) >= 3
    assert plan["requires_executive_summary"] is True