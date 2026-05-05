from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.schemas import StressTestResponse, AttackResult, HallucinationCheckResponse

client = TestClient(app)

MOCK_STRESS = StressTestResponse(
    attacks=[AttackResult(input="bad", attack_type="injection", verdict="PASS", reason="broke it")],
    vulnerability_score=4,
)

MOCK_HALLUCINATION = HallucinationCheckResponse(
    sample_output="some output",
    hallucination_score=8,
    verdict="Low hallucination risk",
    reason="accurate",
)


@patch("backend.routes.advanced.run_stress_test", return_value=MOCK_STRESS)
def test_stress_test_endpoint(mock_fn):
    resp = client.post("/stress-test", json={"prompt": "test", "num_attacks": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["vulnerability_score"] == 4
    assert len(data["attacks"]) == 1
    mock_fn.assert_called_once_with("test", num_attacks=3)


@patch("backend.routes.advanced.check_hallucination", return_value=MOCK_HALLUCINATION)
def test_hallucination_check_endpoint(mock_fn):
    resp = client.post("/hallucination-check", json={"prompt": "Explain DNA"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["hallucination_score"] == 8
    assert data["verdict"] == "Low hallucination risk"


def test_stress_test_missing_prompt_returns_422():
    resp = client.post("/stress-test", json={"num_attacks": 3})
    assert resp.status_code == 422


def test_hallucination_check_missing_prompt_returns_422():
    resp = client.post("/hallucination-check", json={})
    assert resp.status_code == 422
