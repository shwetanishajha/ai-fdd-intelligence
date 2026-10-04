import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.agents.agentic_fdd import run_agentic_fdd


def run_agentic_evaluation():
    with open(
        "evaluation/agentic_questions.json",
        "r",
        encoding="utf-8",
    ) as file:
        questions = json.load(file)

    results = []

    for item in questions:
        result = run_agentic_fdd(
            item["question"]
        )

        executed_agents = [
            agent["agent"]
            for agent in result["results"]
        ]

        agent_match = (
            item["expected_agent"]
            in executed_agents
        )

        output_text = json.dumps(
            result,
            ensure_ascii=False,
        )

        evidence_match = (
            item["expected_text"]
            in output_text
        )

        passed = (
            agent_match
            and evidence_match
        )

        results.append(
            {
                "question": item["question"],
                "agent_match": agent_match,
                "evidence_match": evidence_match,
                "passed": passed,
            }
        )

    passed_count = sum(
        result["passed"]
        for result in results
    )

    print(
        f"Agentic Evaluation: "
        f"{passed_count}/{len(results)} passed"
    )

    for result in results:
        print(
            f"{'PASS' if result['passed'] else 'FAIL'} - "
            f"{result['question']}"
        )


if __name__ == "__main__":
    run_agentic_evaluation()