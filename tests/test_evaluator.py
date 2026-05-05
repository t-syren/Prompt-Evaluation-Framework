from unittest.mock import patch, MagicMock
from backend.services.evaluator import evaluate_prompt, evaluate_dimensions, evaluate_safety
from backend.models.schemas import EvaluateResponse


def _make_geval_mock(score: float, reason: str):
    m = MagicMock()
    m.score = score
    m.reason = reason
    return m


def _make_safety_mock(score: float):
    m = MagicMock()
    m.score = score
    m.reason = "test reason"
    return m


@patch("backend.services.evaluator.GEval")
@patch("backend.services.evaluator.get_deepeval_model")
def test_evaluate_dimensions_returns_6(mock_model, mock_geval_cls):
    instance = _make_geval_mock(0.7, "good clarity")
    mock_geval_cls.return_value = instance
    result = evaluate_dimensions("Write a summary")
    assert len(result) == 6
    assert result[0].name == "Clarity & Specificity"
    # 0.7 * 9 + 1 = 7.3 -> round -> 7
    assert result[0].score == 7
    assert result[0].reasoning == "good clarity"


@patch("backend.services.evaluator.BiasMetric")
@patch("backend.services.evaluator.ToxicityMetric")
@patch("backend.services.evaluator.get_deepeval_model")
def test_evaluate_safety_returns_2(mock_model, mock_tox_cls, mock_bias_cls):
    mock_bias_cls.return_value = _make_safety_mock(0.1)
    mock_tox_cls.return_value = _make_safety_mock(0.0)
    result = evaluate_safety("Write a summary")
    assert len(result) == 2
    assert result[0].name == "Bias"
    assert result[1].name == "Toxicity"
    # bias 0.1 -> (1 - 0.1) * 9 + 1 = 9.1 -> round -> 9
    assert result[0].score == 9
    # toxicity 0.0 -> (1 - 0.0) * 9 + 1 = 10.0 -> round -> 10
    assert result[1].score == 10


@patch("backend.services.evaluator.evaluate_safety")
@patch("backend.services.evaluator.evaluate_dimensions")
def test_evaluate_prompt_returns_8_dimensions(mock_dims, mock_safety):
    from backend.models.schemas import Dimension
    mock_dims.return_value = [
        Dimension(name=f"D{i}", score=7, issues=[], suggestions=[]) for i in range(6)
    ]
    mock_safety.return_value = [
        Dimension(name="Bias", score=9, issues=[], suggestions=[]),
        Dimension(name="Toxicity", score=10, issues=[], suggestions=[]),
    ]
    result = evaluate_prompt("test")
    assert isinstance(result, EvaluateResponse)
    assert len(result.dimensions) == 8


@patch("backend.services.evaluator.BiasMetric")
@patch("backend.services.evaluator.ToxicityMetric")
@patch("backend.services.evaluator.get_deepeval_model")
def test_high_bias_scores_low(mock_model, mock_tox_cls, mock_bias_cls):
    mock_bias_cls.return_value = _make_safety_mock(0.9)
    mock_tox_cls.return_value = _make_safety_mock(0.0)
    result = evaluate_safety("biased prompt")
    # bias 0.9 -> (1 - 0.9) * 9 + 1 = 1.9 -> round -> 2
    assert result[0].score == 2
    assert "Potential bias" in result[0].issues[0]


@patch("backend.services.evaluator.GEval")
@patch("backend.services.evaluator.get_deepeval_model")
def test_normalise_score_boundaries(mock_model, mock_geval_cls):
    # score 0.0 -> 0*9+1 = 1
    mock_geval_cls.return_value = _make_geval_mock(0.0, "bad")
    result = evaluate_dimensions("x")
    assert all(d.score == 1 for d in result)
