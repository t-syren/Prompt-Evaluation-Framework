from unittest.mock import patch, MagicMock
from backend.services.hallucination import check_hallucination
from backend.models.schemas import HallucinationCheckResponse


def _make_geval_metric(score: float, reason: str):
    m = MagicMock()
    m.score = score
    m.reason = reason
    return m


@patch("backend.services.hallucination.GEval")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="A sample LLM output about the topic.")
def test_check_hallucination_returns_response(mock_cc, mock_model, mock_metric_cls):
    mock_metric_cls.return_value = _make_geval_metric(0.9, "Mostly grounded")
    result = check_hallucination("Explain photosynthesis in 2 sentences")
    assert isinstance(result, HallucinationCheckResponse)
    assert result.sample_output == "A sample LLM output about the topic."
    # score: 0.9 * 9 + 1 = 9.1 -> 9
    assert result.hallucination_score == 9
    assert "Mostly grounded" in result.reason


@patch("backend.services.hallucination.GEval")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="output")
def test_vague_prompt_scores_low(mock_cc, mock_model, mock_metric_cls):
    # Vague prompt → LLM invents specifics → low groundedness score → low hallucination score
    mock_metric_cls.return_value = _make_geval_metric(0.1, "Many invented specifics")
    result = check_hallucination("write a sql query for redshift")
    # score: 0.1 * 9 + 1 = 1.9 -> 2
    assert result.hallucination_score <= 3


@patch("backend.services.hallucination.GEval")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="output")
def test_verdict_low_risk_for_high_score(mock_cc, mock_model, mock_metric_cls):
    mock_metric_cls.return_value = _make_geval_metric(0.95, "Fully grounded")
    result = check_hallucination("test prompt")
    assert result.verdict == "Low hallucination risk"


@patch("backend.services.hallucination.GEval")
@patch("backend.services.hallucination.get_deepeval_model")
@patch("backend.services.hallucination.chat_complete", return_value="output")
def test_verdict_high_risk_for_low_score(mock_cc, mock_model, mock_metric_cls):
    mock_metric_cls.return_value = _make_geval_metric(0.05, "Heavy hallucination")
    result = check_hallucination("test prompt")
    assert result.verdict == "High hallucination risk"
