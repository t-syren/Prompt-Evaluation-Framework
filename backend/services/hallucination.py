from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from backend.services.databricks_client import chat_complete
from backend.services.deepeval_client import get_deepeval_model
from backend.models.schemas import HallucinationCheckResponse


def check_hallucination(prompt: str) -> HallucinationCheckResponse:
    sample_output = chat_complete(
        [{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    model = get_deepeval_model()
    metric = HallucinationMetric(threshold=0.5, model=model)
    test_case = LLMTestCase(
        input=prompt,
        actual_output=sample_output,
        context=[prompt],
    )
    metric.measure(test_case)

    raw = metric.score
    score = max(1, min(10, round((1 - raw) * 9) + 1))

    if score >= 8:
        verdict = "Low hallucination risk"
    elif score >= 5:
        verdict = "Moderate hallucination risk"
    else:
        verdict = "High hallucination risk"

    return HallucinationCheckResponse(
        sample_output=sample_output,
        hallucination_score=score,
        verdict=verdict,
        reason=metric.reason or "",
    )
