from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


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