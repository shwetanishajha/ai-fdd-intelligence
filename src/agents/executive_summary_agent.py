import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

load_dotenv()

client = OpenAI()


class KeyRisk(BaseModel):
    risk: str
    evidence: str


class ExecutiveSummary(BaseModel):
    executive_summary: str
    key_risks: list[KeyRisk] = Field(min_length=1)
    further_diligence: list[str] = Field(min_length=1)
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
You are a senior financial due diligence advisor.

Review the findings produced by specialist FDD agents below.

Identify:
1. The most important financial risks
2. The key supporting evidence for each risk
3. Areas requiring further diligence
4. An overall risk assessment

Do not invent facts.
Use only the findings provided.

The overall_risk MUST be exactly one of:
- Low
- Medium
- High

Each key risk must contain:
- risk
- evidence

Specialist findings:
{json.dumps(agent_results, ensure_ascii=False, indent=2)}

Return valid JSON with exactly these fields:
- executive_summary
- key_risks
- further_diligence
- overall_risk

The key_risks field must be an array of objects.
Each object must contain "risk" and "evidence".
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence-based financial "
                    "due diligence executive summarisation agent."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    summary = ExecutiveSummary.model_validate(
        json.loads(response.choices[0].message.content)
    )

    return summary.model_dump()