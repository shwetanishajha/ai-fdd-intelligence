import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.retrieval.search import search_documents


def run_evaluation():
    with open("evaluation/questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)

    results = []

    for item in questions:
        retrieved = search_documents(item["question"])

        source_match = any(
            result["source"] == item["expected_source"]
            and result["page"] == item["expected_page"]
            for result in retrieved
        )

        if item["question"] == "What areas require further diligence?":
            required_topics = [
                "Customer concentration",
                "Revenue quality",
                "EBITDA sustainability",
                "Working capital movements",
                "Cost trends",
            ]

            retrieved_text = " ".join(
                result["text"] for result in retrieved
            )

            evidence_match = all(
                topic in retrieved_text
                for topic in required_topics
            )

        else:
            expected = " ".join(
                item["expected_evidence"].split()
            )

            evidence_match = any(
                expected in " ".join(result["text"].split())
                for result in retrieved
            )

        results.append({
            "question": item["question"],
            "source_match": source_match,
            "evidence_match": evidence_match,
            "passed": source_match and evidence_match,
        })

    passed = sum(result["passed"] for result in results)

    print(f"Evaluation: {passed}/{len(results)} passed")

    for result in results:
        print(
            f"{'PASS' if result['passed'] else 'FAIL'} - "
            f"{result['question']}"
        )


if __name__ == "__main__":
    run_evaluation()