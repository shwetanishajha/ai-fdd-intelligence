from src.agents.models import FDDFinding


def review_finding(
    finding: dict,
    decision: str,
    amended_finding: str | None = None,
) -> dict:
    decision = decision.capitalize()

    if decision not in {"Approved", "Rejected", "Amended"}:
        raise ValueError(
            "decision must be Approved, Rejected, or Amended"
        )

    validated = FDDFinding.model_validate(finding)

    if decision == "Amended":
        if not amended_finding:
            raise ValueError(
                "amended_finding is required when decision is Amended"
            )
        validated.finding = amended_finding

    validated.human_review_status = decision

    return validated.model_dump()