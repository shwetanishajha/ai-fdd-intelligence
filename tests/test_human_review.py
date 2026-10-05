import pytest

from src.validation.human_review import review_finding


def sample_finding():
    return {
        "finding": "Customer A represents 38% of FY2025 revenue.",
        "risk_level": "High",
        "evidence": "Customer A generated £20.52 million of revenue.",
        "source": "fdd_report.pdf",
        "page": 1,
        "confidence": 0.95,
    }


def test_approve_finding():
    result = review_finding(
        sample_finding(),
        "Approved",
    )

    assert result["human_review_status"] == "Approved"
    assert result["finding"] == sample_finding()["finding"]


def test_reject_finding():
    result = review_finding(
        sample_finding(),
        "Rejected",
    )

    assert result["human_review_status"] == "Rejected"


def test_amend_finding():
    result = review_finding(
        sample_finding(),
        "Amended",
        amended_finding="Customer A represents a material concentration risk.",
    )

    assert result["human_review_status"] == "Amended"
    assert result["finding"] == (
        "Customer A represents a material concentration risk."
    )


def test_amend_requires_text():
    with pytest.raises(ValueError):
        review_finding(
            sample_finding(),
            "Amended",
        )


def test_invalid_review_decision():
    with pytest.raises(ValueError):
        review_finding(
            sample_finding(),
            "Maybe",
        )