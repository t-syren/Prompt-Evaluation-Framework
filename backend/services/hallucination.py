from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase
try:
    from deepeval.test_case import SingleTurnParams as _EvalParams
except ImportError:
    from deepeval.test_case import LLMTestCaseParams as _EvalParams  # type: ignore
from backend.services.databricks_client import chat_complete
from backend.services.deepeval_client import get_deepeval_model
from backend.models.schemas import HallucinationCheckResponse

_HALLUCINATION_CRITERIA = (
    "You are evaluating whether an LLM's output contains hallucinated content. "
    "The 'input' is the original prompt given to the LLM. "
    "The 'actual output' is what the LLM generated. "
    "\n\n"
    "Hallucination means the LLM invented specific details that were NOT specified or implied "
    "by the prompt and cannot be verified from the prompt alone. Examples of invented specifics: "
    "table names, column names, function names, URLs, statistics, version numbers, variable names, "
    "configuration values, API keys, or any other concrete named entity. "
    "\n\n"
    "Score 1.0 (fully grounded): Every specific detail in the output is either explicitly stated "
    "in the prompt or is a universally agreed-upon fact. Nothing was invented. "
    "\n\n"
    "Score 0.0 (heavy hallucination): The output is full of invented specifics. For example, "
    "a vague prompt like 'write a SQL query for Redshift' causes the LLM to invent table names, "
    "column names, WHERE clauses, etc. that were never requested — all hallucinated. "
    "\n\n"
    "Be strict: if the prompt does not specify table names but the output contains them, "
    "those are hallucinated. If the prompt says 'users table', then 'users' is grounded."
)


def check_hallucination(prompt: str) -> HallucinationCheckResponse:
    sample_output = chat_complete(
        [{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    model = get_deepeval_model()
    metric = GEval(
        name="Hallucination Risk",
        criteria=_HALLUCINATION_CRITERIA,
        evaluation_params=[_EvalParams.INPUT, _EvalParams.ACTUAL_OUTPUT],
        model=model,
        strict_mode=False,
    )
    metric.measure(LLMTestCase(input=prompt, actual_output=sample_output))

    # GEval 0-1 where 1.0 = fully grounded (no hallucination), 0.0 = heavy hallucination
    raw = metric.score
    # Map to 1-10: high raw → high score (low risk), low raw → low score (high risk)
    score = max(1, min(10, round(raw * 9) + 1))

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
