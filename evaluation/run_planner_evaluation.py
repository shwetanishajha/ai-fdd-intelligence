import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.agents.planner import create_fdd_plan


def run_planner_evaluation():
    with open(
        "evaluation/planner_questions.json",
        "r",
        encoding="utf-8",
    ) as file:
        questions = json.load(file)

    results = []

    for item in questions:
        plan = create_fdd_plan(
            item["question"]
        )

        selected_agents = set(
            plan["selected_agents"]
        )

        expected_agents = set(
            item["expected_agents"]
        )

        agents_match = (
            selected_agents == expected_agents
        )

        results.append(
            {
                "question": item["question"],
                "expected_agents": list(
                    expected_agents
                ),
                "selected_agents": list(
                    selected_agents
                ),
                "agents_match": agents_match,
                "passed": agents_match,
            }
        )

    passed = sum(
        result["passed"]
        for result in results
    )

    print(
        f"Planner Evaluation: "
        f"{passed}/{len(results)} passed"
    )

    for result in results:
        print(
            f"{'PASS' if result['passed'] else 'FAIL'} - "
            f"{result['question']}"
        )

        if not result["passed"]:
            print(
                f"  Expected: "
                f"{result['expected_agents']}"
            )
            print(
                f"  Selected: "
                f"{result['selected_agents']}"
            )


if __name__ == "__main__":
    run_planner_evaluation()