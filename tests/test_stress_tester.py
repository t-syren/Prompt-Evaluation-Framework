import json
from unittest.mock import patch
from backend.services.stress_tester import run_stress_test
from backend.models.schemas import StressTestResponse

MOCK_ATTACK = '{"verdict": "PASS", "reason": "Successfully changed intent"}'
MOCK_BENIGN = '{"verdict": "FAIL", "reason": "Intent preserved"}'


@patch("backend.services.stress_tester.chat_complete")
def test_run_stress_test_returns_response(mock_cc):
    # First call = generate attack, second call = verdict
    mock_cc.side_effect = ["injected adversarial prompt", MOCK_ATTACK] * 3
    result = run_stress_test("Write a poem about spring", num_attacks=3)
    assert isinstance(result, StressTestResponse)
    assert len(result.attacks) == 3
    assert result.vulnerability_score >= 1
    assert result.vulnerability_score <= 10


@patch("backend.services.stress_tester.chat_complete")
def test_vulnerability_score_high_when_all_pass(mock_cc):
    mock_cc.side_effect = ["adversarial", MOCK_ATTACK] * 5
    result = run_stress_test("test prompt", num_attacks=5)
    # All 5 attacks succeeded -> very vulnerable -> low score
    assert result.vulnerability_score <= 3


@patch("backend.services.stress_tester.chat_complete")
def test_vulnerability_score_low_when_none_pass(mock_cc):
    mock_cc.side_effect = ["adversarial", MOCK_BENIGN] * 5
    result = run_stress_test("test prompt", num_attacks=5)
    # No attacks succeeded -> robust -> high score
    assert result.vulnerability_score >= 8
