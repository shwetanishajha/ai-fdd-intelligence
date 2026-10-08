import json

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

from src.core.llm_client import call_llm

load_dotenv()


class KeyRisk(BaseModel):
    risk: str
    evidence: str


class ExecutiveSummary(BaseModel):
    executive_summary: str | dict
    key_risks: list[KeyRisk] = Field(min_length=1)
    further_diligence: list[str] | dict
    overall_risk: str

    @field_validator("overall_risk")
    @classmethod
    def validate_overall_risk(cls, value: str) -> str:
        value = value.capitalize()

        if value not in {"Low", "Medium", "High"}:
            raise ValueError(
                "overall_risk must be Low, Medium, or High"
            )

        return value


def create_executive_summary(agent_results: list[dict]) -> dict:

    prompt = f"""
You are a senior financial due diligence analyst.

Create an executive summary using ONLY the specialist findings
provided below.

Do not invent facts or numbers.

Specialist findings:
{json.dumps(agent_results, ensure_ascii=False, indent=2)}

Return valid JSON with exactly these fields:
- executive_summary
- key_risks
- further_diligence
- overall_risk

Each key risk must contain:
- risk
- evidence

Overall risk must be one of:
- Low
- Medium
- High
"""

    response = call_llm(
        messages=[
            {
                "role": "system",
                "content": (
                    "You produce evidence-based financial "
                    "due diligence executive summaries."
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

    summary = ExecutiveSummary.model_validate(
        json.loads(response.choices[0].message.content)
    )

    return summary.model_dump()