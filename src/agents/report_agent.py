import json

from dotenv import load_dotenv

from src.agents.models import FDDReport
from src.core.llm_client import call_llm

load_dotenv()


def create_fdd_report(agent_results: list[dict]) -> dict:

    prompt = f"""
You are a senior financial due diligence report writer.

Create a structured FDD report using ONLY the specialist findings
provided below.

Do not invent facts or numbers.

Populate these sections:
- executive_summary
- company_overview
- revenue_analysis
- ebitda_analysis
- working_capital_analysis
- customer_concentration
- financial_anomalies
- key_risks
- further_diligence
- evidence_register

Each key risk must contain:
- risk
- evidence

Preserve evidence and source information from the specialist findings.

Specialist findings:
{json.dumps(agent_results, ensure_ascii=False, indent=2)}

Return valid JSON matching the FDDReport schema.
"""

    response = call_llm(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence-based financial "
                    "due diligence report generation agent."
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

    report = FDDReport.model_validate(
        json.loads(response.choices[0].message.content)
    )

    return report.model_dump()