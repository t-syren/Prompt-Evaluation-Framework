from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.models.schemas import EvaluateResponse, Dimension
from backend.main import app

client = TestClient(app)

MOCK_EVAL = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=7, issues=[], suggestions=["Be more specific"]),
    Dimension(name="Role / Persona Definition", score=5, issues=["No role"], suggestions=["Add role"]),
    Dimension(name="Output Format Instructions", score=6, issues=[], suggestions=[]),
    Dimension(name="Context & Background", score=8, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=9, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=7, issues=[], suggestions=[]),
])


def test_evaluate_returns_200_with_dimensions():
    with patch("backend.routes.evaluate.evaluate_prompt", return_value=MOCK_EVAL):
        response = client.post("/evaluate", json={"prompt": "Write a summary"})
    assert response.status_code == 200
    data = response.json()
    assert "dimensions" in data
    assert len(data["dimensions"]) == 6


def test_evaluate_empty_prompt_returns_422():
    response = client.post("/evaluate", json={"prompt": ""})
    assert response.status_code == 422


def test_evaluate_missing_prompt_returns_422():
    response = client.post("/evaluate", json={})
    assert response.status_code == 422


def test_evaluate_llm_error_returns_503():
    with patch("backend.routes.evaluate.evaluate_prompt", side_effect=Exception("LLM unreachable")):
        response = client.post("/evaluate", json={"prompt": "Some prompt"})
    assert response.status_code == 503


MOCK_DIMS = [
    Dimension(name=f"D{i}", score=7, issues=[], suggestions=[], reasoning="ok")
    for i in range(6)
]
MOCK_SAFETY = [
    Dimension(name="Bias", score=9, issues=[], suggestions=[], reasoning=""),
    Dimension(name="Toxicity", score=10, issues=[], suggestions=[], reasoning=""),
]


@patch("backend.routes.evaluate.evaluate_dimensions", return_value=MOCK_DIMS)
def test_evaluate_dimensions_endpoint(mock_fn):
    resp = client.post("/evaluate/dimensions", json={"prompt": "test prompt"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["dimensions"]) == 6
    assert data["dimensions"][0]["reasoning"] == "ok"


@patch("backend.routes.evaluate.evaluate_safety", return_value=MOCK_SAFETY)
def test_evaluate_safety_endpoint(mock_fn):
    resp = client.post("/evaluate/safety", json={"prompt": "test prompt"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["dimensions"]) == 2
    assert data["dimensions"][0]["name"] == "Bias"
