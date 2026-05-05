import pytest
from backend.models.schemas import (
    EvaluatRequest,
    Dimension,
    EvaluateResponse,
    FixRequest,
    FixResponse,
    ExportRequest,
    ConfigModel,
    ConfigResponse,
)


def test_evaluate_request_valid():
    req = EvaluatRequest(prompt="Tell me a joke")
    assert req.prompt == "Tell me a joke"


def test_evaluate_request_empty_prompt_fails():
    with pytest.raises(Exception):
        EvaluatRequest(prompt="")


def test_dimension_valid():
    d = Dimension(
        name="Clarity",
        score=7,
        issues=["Too vague"],
        suggestions=["Be more specific"],
    )
    assert d.score == 7


def test_dimension_score_out_of_range():
    with pytest.raises(Exception):
        Dimension(name="Clarity", score=11, issues=[], suggestions=[])


def test_evaluate_response_valid():
    resp = EvaluateResponse(
        dimensions=[
            Dimension(name="Clarity", score=8, issues=[], suggestions=[])
        ]
    )
    assert len(resp.dimensions) == 1


def test_fix_request_single_mode():
    req = FixRequest(
        prompt="Write code",
        evaluation=EvaluateResponse(dimensions=[]),
        mode="single",
    )
    assert req.mode == "single"


def test_fix_request_invalid_mode():
    with pytest.raises(Exception):
        FixRequest(
            prompt="Write code",
            evaluation=EvaluateResponse(dimensions=[]),
            mode="invalid",
        )


def test_fix_response_single():
    resp = FixResponse(fixed_prompt="Improved prompt")
    assert resp.fixed_prompt == "Improved prompt"
    assert resp.variants is None


def test_fix_response_variants():
    resp = FixResponse(variants=["v1", "v2", "v3"])
    assert len(resp.variants) == 3
    assert resp.fixed_prompt is None


def test_config_model_valid():
    cfg = ConfigModel(
        databricks_base_url="https://example.com",
        llm_endpoint_url="https://example.com/invocations",
        api_token="dapi123",
    )
    assert cfg.api_token == "dapi123"


def test_config_response_masks_token():
    resp = ConfigResponse(
        databricks_base_url="https://example.com",
        llm_endpoint_url="https://example.com/invocations",
        api_token_set=True,
    )
    assert resp.api_token_set is True


# ── New schema tests (DeepEval integration) ───────────────────────────────────
from backend.models.schemas import (  # noqa: E402
    DefaultsConfig, StressTestRequest, StressTestResponse,
    AttackResult, HallucinationCheckRequest, HallucinationCheckResponse,
    FixValidateRequest, FixValidateResponse, RegressionWarning,
)


def test_dimension_reasoning_is_optional():
    d = Dimension(name="Clarity & Specificity", score=7, issues=[], suggestions=[])
    assert d.reasoning is None


def test_dimension_accepts_reasoning():
    d = Dimension(name="Clarity & Specificity", score=7, issues=[], suggestions=[], reasoning="Good prompt")
    assert d.reasoning == "Good prompt"


def test_defaults_config_defaults():
    cfg = DefaultsConfig()
    assert cfg.auto_evaluate_after_fix is True
    assert cfg.auto_stress_test is False
    assert cfg.auto_hallucination_check is False
    assert cfg.stress_test_attack_count == 5
    assert cfg.iterative_fix_passes == 2


def test_stress_test_request():
    req = StressTestRequest(prompt="test", num_attacks=3)
    assert req.num_attacks == 3


def test_stress_test_response():
    resp = StressTestResponse(
        attacks=[AttackResult(input="bad", attack_type="injection", verdict="PASS", reason="broke it")],
        vulnerability_score=8,
    )
    assert resp.vulnerability_score == 8


def test_hallucination_check_response():
    resp = HallucinationCheckResponse(
        sample_output="some output",
        hallucination_score=9,
        verdict="Low risk",
        reason="Accurate",
    )
    assert resp.hallucination_score == 9


def test_fix_validate_response():
    dims = [Dimension(name="Clarity & Specificity", score=8, issues=[], suggestions=[])]
    ev = EvaluateResponse(dimensions=dims)
    resp = FixValidateResponse(
        post_eval=ev,
        regression_warnings=[RegressionWarning(dimension="Clarity & Specificity", original_score=9, fixed_score=8)],
        safety_warnings=[],
    )
    assert len(resp.regression_warnings) == 1
