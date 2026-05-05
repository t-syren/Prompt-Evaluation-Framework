import json
from fastapi.testclient import TestClient
from backend.models.schemas import EvaluateResponse, Dimension
from backend.main import app

client = TestClient(app)

SAMPLE_EVAL = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=7, issues=[], suggestions=[]),
    Dimension(name="Role / Persona Definition", score=5, issues=[], suggestions=[]),
    Dimension(name="Output Format Instructions", score=6, issues=[], suggestions=[]),
    Dimension(name="Context & Background", score=8, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=9, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=7, issues=[], suggestions=[]),
])


def test_export_returns_json_file():
    payload = {
        "original_prompt": "Write a summary",
        "evaluation": SAMPLE_EVAL.model_dump(),
        "fixed_prompt": "You are an expert. Write a concise summary.",
        "mode": "single",
    }
    response = client.post("/export", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = json.loads(response.content)
    assert data["original_prompt"] == "Write a summary"
    assert "timestamp" in data
    assert data["mode"] == "single"


def test_export_includes_variants_when_provided():
    payload = {
        "original_prompt": "Write a summary",
        "evaluation": SAMPLE_EVAL.model_dump(),
        "variants": ["v1", "v2", "v3"],
        "mode": "variants",
    }
    response = client.post("/export", json=payload)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["variants"] == ["v1", "v2", "v3"]
