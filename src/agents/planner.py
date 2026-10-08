import json

from pydantic import BaseModel, Field

from src.core.llm_client import call_llm


ALLOWED_AGENTS = {
    "Revenue Agent",
    "EBITDA Agent",
    "Working Capital Agent",
    "Customer Concentration Agent",
    "Financial Anomaly Agent",
}


class FDDPlan(BaseModel):
    reasoning: str
    selected_agents: list[str] = Field(min_length=1)
    requires_executive_summary: bool = True


def create_fdd_plan(question: str) -> dict:
    prompt = f"""
You are an FDD task planner.

Analyze the user's financial due diligence question and determine
which specialist agents are required.

Available agents:
- Revenue Agent
- EBITDA Agent
- Working Capital Agent
- Customer Concentration Agent
- Financial Anomaly Agent

Rules:
- Select only agents from the available list.
- Select the minimum agents necessary to answer the question.
- If the question asks for an overall assessment, key risks,
  overall FDD, or key findings, select all relevant agents.
- Do not answer the financial question yourself.
- Return only a JSON execution plan.

User question:
{question}

Return JSON with exactly these fields:
- reasoning
- selected_agents
- requires_executive_summary
"""

    response = call_llm(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a controlled financial due diligence "
                    "task planner."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
    )

    plan = FDDPlan.model_validate(
        json.loads(response.choices[0].message.content)
    )

    invalid_agents = set(plan.selected_agents) - ALLOWED_AGENTS

    if invalid_agents:
        raise ValueError(
            f"Planner selected unsupported agents: {invalid_agents}"
        )

    return plan.model_dump()