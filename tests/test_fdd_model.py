import pytest
from pydantic import ValidationError

from src.agents.models import FDDFinding


def test_valid_fdd_finding():
    finding = FDDFinding(
        finding="Customer concentration is significant.",
        risk_level="high",
        evidence="Customer A represents 38% of revenue.",
        source="fdd_report.pdf",
        page=1,
        confidence=0.92,
    )

    assert finding.risk_level == "High"
    assert finding.confidence == 0.92
    assert finding.human_review_status == "Pending"


def test_invalid_confidence():
    with pytest.raises(ValidationError):
        FDDFinding(
            finding="Test finding",
            risk_level="Low",
            evidence="Test evidence",
            source="test.pdf",
            page=1,
            confidence=1.5,
        )


def test_invalid_risk_level():
    with pytest.raises(ValidationError):
        FDDFinding(
            finding="Test finding",
            risk_level="Critical",
            evidence="Test evidence",
            source="test.pdf",
            page=1,
            confidence=0.8,
        )