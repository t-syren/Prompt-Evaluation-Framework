from unittest.mock import patch, MagicMock
from backend.services.hallucination import check_hallucination
from backend.models.schemas import HallucinationCheckResponse


def _make_hallucination_metric(score: float, reason: str):
    m = MagicMock()
    m.score = score
    m.reason = reason
    return m


@patch("backend.services.hallucination.HallucinationMetric")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="A sample LLM output about the topic.")
def test_check_hallucination_returns_response(mock_cc, mock_model, mock_metric_cls):
    mock_metric_cls.return_value = _make_hallucination_metric(0.1, "Mostly accurate")
    result = check_hallucination("Explain photosynthesis in 2 sentences")
    assert isinstance(result, HallucinationCheckResponse)
    assert result.sample_output == "A sample LLM output about the topic."
    # score: (1 - 0.1) * 9 + 1 = 9.1 -> 9
    assert result.hallucination_score == 9
    assert "Mostly accurate" in result.reason


@patch("backend.services.hallucination.HallucinationMetric")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="output")
def test_high_hallucination_scores_low(mock_cc, mock_model, mock_metric_cls):
    mock_metric_cls.return_value = _make_hallucination_metric(0.9, "Very likely to hallucinate")
    result = check_hallucination("test prompt")
    # score: (1 - 0.9) * 9 + 1 = 1.9 -> 2
    assert result.hallucination_score <= 3


@patch("backend.services.hallucination.HallucinationMetric")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="output")
def test_verdict_low_risk_for_high_score(mock_cc, mock_model, mock_metric_cls):
    mock_metric_cls.return_value = _make_hallucination_metric(0.05, "Accurate")
    result = check_hallucination("test prompt")
    assert result.verdict == "Low hallucination risk"


@patch("backend.services.hallucination.HallucinationMetric")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="output")
def test_verdict_high_risk_for_low_score(mock_cc, mock_model, mock_metric_cls):
    mock_metric_cls.return_value = _make_hallucination_metric(0.95, "Highly inaccurate")
    result = check_hallucination("test prompt")
    assert result.verdict == "High hallucination risk"
