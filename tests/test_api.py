from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_agentic_fdd_endpoint():
    response = client.get(
        "/fdd/agentic",
        params={
            "question": "What was the FY2025 EBITDA margin?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "plan" in data
    assert "results" in data
    assert "execution" in data

    assert "EBITDA Agent" in (
        data["plan"]["selected_agents"]
    )


def test_review_approved_finding():
    finding = {
        "finding": "Customer A represents 38% of FY2025 revenue.",
        "risk_level": "High",
        "evidence": "Customer A generated £20.52 million of revenue.",
        "source": "fdd_report.pdf",
        "page": 1,
        "confidence": 0.95,
    }

    response = client.post(
        "/fdd/review",
        json={
            "finding": finding,
            "decision": "Approved",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["human_review_status"] == "Approved"


def test_review_rejected_finding():
    finding = {
        "finding": "Customer A represents 38% of FY2025 revenue.",
        "risk_level": "High",
        "evidence": "Customer A generated £20.52 million of revenue.",
        "source": "fdd_report.pdf",
        "page": 1,
        "confidence": 0.95,
    }

    response = client.post(
        "/fdd/review",
        json={
            "finding": finding,
            "decision": "Rejected",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["human_review_status"] == "Rejected"


def test_review_amended_finding():
    finding = {
        "finding": "Customer A represents 38% of FY2025 revenue.",
        "risk_level": "High",
        "evidence": "Customer A generated £20.52 million of revenue.",
        "source": "fdd_report.pdf",
        "page": 1,
        "confidence": 0.95,
    }

    amended_text = (
        "Customer A represents a material concentration risk."
    )

    response = client.post(
        "/fdd/review",
        json={
            "finding": finding,
            "decision": "Amended",
            "amended_finding": amended_text,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["human_review_status"] == "Amended"
    assert data["finding"] == amended_text