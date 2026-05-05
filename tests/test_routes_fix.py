from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.models.schemas import EvaluateResponse, Dimension, FixResponse
from backend.main import app

client = TestClient(app)

SAMPLE_EVAL = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=5, issues=["vague"], suggestions=["be specific"]),
    Dimension(name="Role / Persona Definition", score=3, issues=["no role"], suggestions=["add role"]),
    Dimension(name="Output Format Instructions", score=4, issues=[], suggestions=[]),
    Dimension(name="Context & Background", score=6, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=7, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=5, issues=[], suggestions=[]),
])

FIX_PAYLOAD_SINGLE = {
    "prompt": "Summarize this.",
    "evaluation": SAMPLE_EVAL.model_dump(),
    "mode": "single",
}

FIX_PAYLOAD_VARIANTS = {
    "prompt": "Summarize this.",
    "evaluation": SAMPLE_EVAL.model_dump(),
    "mode": "variants",
}


def test_fix_single_returns_fixed_prompt():
    mock_result = FixResponse(fixed_prompt="You are an expert. Summarize in 3 bullet points.")
    with patch("backend.routes.fix.fix_prompt", return_value=mock_result):
        response = client.post("/fix", json=FIX_PAYLOAD_SINGLE)
    assert response.status_code == 200
    assert "fixed_prompt" in response.json()


def test_fix_variants_returns_three_variants():
    mock_result = FixResponse(variants=["v1", "v2", "v3"])
    with patch("backend.routes.fix.fix_prompt", return_value=mock_result):
        response = client.post("/fix", json=FIX_PAYLOAD_VARIANTS)
    assert response.status_code == 200
    assert len(response.json()["variants"]) == 3


def test_fix_invalid_mode_returns_422():
    payload = {**FIX_PAYLOAD_SINGLE, "mode": "unknown"}
    response = client.post("/fix", json=payload)
    assert response.status_code == 422


def test_fix_llm_error_returns_503():
    with patch("backend.routes.fix.fix_prompt", side_effect=Exception("LLM down")):
        response = client.post("/fix", json=FIX_PAYLOAD_SINGLE)
    assert response.status_code == 503
