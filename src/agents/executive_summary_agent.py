from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()


def create_executive_summary(agent_results: list[dict]) -> dict:
    prompt = f"""
You are a senior financial due diligence advisor.

Review the findings produced by specialist FDD agents below.

Identify:
1. The most important financial risks
2. The key supporting evidence
3. Areas requiring further diligence
4. An overall risk assessment

Do not invent facts.
Use only the findings provided.

Specialist findings:
{json.dumps(agent_results, ensure_ascii=False, indent=2)}

Return valid JSON with exactly these fields:
- executive_summary
- key_risks
- further_diligence
- overall_risk
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence-based financial due diligence "
                    "executive summarisation agent."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return json.loads(response.choices[0].message.content)