import json
import pytest
from unittest.mock import patch
from backend.services.fixer import fix_prompt
from backend.models.schemas import EvaluateResponse, Dimension, FixResponse

SAMPLE_EVALUATION = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=5, issues=["Too vague"], suggestions=["Be specific"]),
    Dimension(name="Role / Persona Definition", score=3, issues=["No role"], suggestions=["Add a role"]),
    Dimension(name="Output Format Instructions", score=4, issues=["No format"], suggestions=["Add format"]),
    Dimension(name="Context & Background", score=6, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=7, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=5, issues=["Tone unclear"], suggestions=["Specify tone"]),
])


def test_fix_single_mode_returns_fixed_prompt():
    with patch("backend.services.fixer.chat_complete", return_value="You are a helpful assistant. Summarize the document in 3 bullet points."):
        result = fix_prompt("Summarize this.", SAMPLE_EVALUATION, mode="single")
    assert isinstance(result, FixResponse)
    assert result.fixed_prompt is not None
    assert result.variants is None


def test_fix_variants_mode_returns_three_variants():
    mock_variants = json.dumps(["Variant 1: improved prompt", "Variant 2: improved prompt", "Variant 3: improved prompt"])
    with patch("backend.services.fixer.chat_complete", return_value=mock_variants):
        result = fix_prompt("Summarize this.", SAMPLE_EVALUATION, mode="variants")
    assert result.variants is not None
    assert len(result.variants) == 3
    assert result.fixed_prompt is None


def test_fix_variants_retries_on_bad_json():
    bad = "not json"
    good = json.dumps(["v1", "v2", "v3"])
    call_count = {"n": 0}

    def mock_chat(messages, temperature=0.2):
        call_count["n"] += 1
        return bad if call_count["n"] == 1 else good

    with patch("backend.services.fixer.chat_complete", side_effect=mock_chat):
        result = fix_prompt("prompt", SAMPLE_EVALUATION, mode="variants")
    assert call_count["n"] == 2
    assert len(result.variants) == 3


def test_fix_variants_raises_after_two_bad_responses():
    with patch("backend.services.fixer.chat_complete", return_value="not json"):
        with pytest.raises(ValueError, match="Failed to parse"):
            fix_prompt("prompt", SAMPLE_EVALUATION, mode="variants")


# ── New tests (DeepEval integration) ─────────────────────────────────────────
from backend.services.fixer import validate_fix  # noqa: E402
from backend.models.schemas import FixValidateResponse  # noqa: E402


def _make_eval(scores: list[int]) -> EvaluateResponse:
    names = ["Clarity & Specificity", "Role / Persona Definition",
             "Output Format Instructions", "Context & Background",
             "Constraints & Guardrails", "Tone & Style", "Bias", "Toxicity"]
    dims = [Dimension(name=names[i], score=s, issues=[], suggestions=[], reasoning=f"reason {i}")
            for i, s in enumerate(scores)]
    return EvaluateResponse(dimensions=dims)


@patch("backend.services.fixer.chat_complete", return_value="improved prompt text")
def test_fix_prompt_single_includes_reasoning(mock_cc):
    evaluation = _make_eval([4, 3, 5, 4, 7, 6, 9, 10])
    result = fix_prompt("original", evaluation, "single")
    call_args = mock_cc.call_args[0][0]
    user_msg = call_args[1]["content"]
    assert "reason 0" in user_msg
    assert result.fixed_prompt == "improved prompt text"


@patch("backend.services.fixer.evaluate_prompt")
def test_validate_fix_returns_regression_warnings(mock_eval):
    original_eval = _make_eval([8, 7, 8, 7, 8, 7, 9, 10])
    post_eval = _make_eval([6, 7, 8, 7, 8, 7, 9, 10])  # Clarity dropped 8->6
    mock_eval.return_value = post_eval
    result = validate_fix("original", "fixed", original_eval)
    assert isinstance(result, FixValidateResponse)
    assert len(result.regression_warnings) == 1
    assert result.regression_warnings[0].dimension == "Clarity & Specificity"
    assert result.regression_warnings[0].original_score == 8
    assert result.regression_warnings[0].fixed_score == 6


@patch("backend.services.fixer.evaluate_prompt")
def test_validate_fix_returns_safety_warnings_when_low(mock_eval):
    original_eval = _make_eval([8, 7, 8, 7, 8, 7, 9, 10])
    post_eval = _make_eval([8, 7, 8, 7, 8, 7, 4, 10])  # Bias dropped to 4
    mock_eval.return_value = post_eval
    result = validate_fix("original", "fixed", original_eval)
    assert "Bias" in result.safety_warnings
