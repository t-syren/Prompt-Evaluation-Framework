from concurrent.futures import ThreadPoolExecutor, as_completed
from deepeval.metrics import GEval, BiasMetric, ToxicityMetric
from deepeval.test_case import LLMTestCase
try:
    from deepeval.test_case import SingleTurnParams as _EvalParams
except ImportError:
    from deepeval.test_case import LLMTestCaseParams as _EvalParams  # type: ignore
from backend.services.deepeval_client import get_deepeval_model
from backend.models.schemas import Dimension, EvaluateResponse

GEVAL_DIMENSIONS = [
    (
        "Clarity & Specificity",
        "Is the prompt unambiguous, precise, and specific about exactly what it wants the model to do? "
        "A clear prompt leaves no room for misinterpretation.",
    ),
    (
        "Role / Persona Definition",
        "Does the prompt establish a clear role, persona, or identity for the model? "
        "E.g. 'You are an expert software engineer'.",
    ),
    (
        "Output Format Instructions",
        "Does the prompt specify the desired output format? "
        "E.g. JSON, markdown, bullet points, a specific number of words.",
    ),
    (
        "Context & Background",
        "Does the prompt provide sufficient context or background information for the model to "
        "complete the task accurately without needing to guess missing information?",
    ),
    (
        "Constraints & Guardrails",
        "Does the prompt clearly state limitations, restrictions, or boundaries? "
        "E.g. 'Do not include X', 'Stay within Y words', 'Only use Z sources'.",
    ),
    (
        "Tone & Style",
        "Does the prompt specify the desired tone, writing style, or register? "
        "E.g. formal, casual, technical, friendly.",
    ),
]


def _normalise_score(raw: float, invert: bool = False) -> int:
    """Convert 0-1 DeepEval score to 1-10 int. Invert for metrics where higher = worse."""
    if invert:
        raw = 1.0 - raw
    return max(1, min(10, round(raw * 9) + 1))


def _run_geval(name: str, criteria: str, prompt: str) -> Dimension:
    model = get_deepeval_model()
    metric = GEval(
        name=name,
        criteria=criteria,
        evaluation_params=[_EvalParams.INPUT],
        model=model,
        strict_mode=False,
    )
    metric.measure(LLMTestCase(input=prompt, actual_output=""))
    return Dimension(
        name=name,
        score=_normalise_score(metric.score),
        issues=[],
        suggestions=[],
        reasoning=metric.reason or "",
    )


def _run_bias(prompt: str) -> Dimension:
    model = get_deepeval_model()
    metric = BiasMetric(threshold=0.5, model=model)
    metric.measure(LLMTestCase(input=prompt, actual_output=prompt))
    return Dimension(
        name="Bias",
        score=_normalise_score(metric.score, invert=True),
        issues=[] if metric.score < 0.5 else ["Potential bias detected in prompt language"],
        suggestions=[] if metric.score < 0.5 else ["Review for neutral, inclusive language"],
        reasoning=metric.reason or "",
    )


def _run_toxicity(prompt: str) -> Dimension:
    model = get_deepeval_model()
    metric = ToxicityMetric(threshold=0.5, model=model)
    metric.measure(LLMTestCase(input=prompt, actual_output=prompt))
    return Dimension(
        name="Toxicity",
        score=_normalise_score(metric.score, invert=True),
        issues=[] if metric.score < 0.5 else ["Potentially harmful language detected"],
        suggestions=[] if metric.score < 0.5 else ["Remove or rephrase harmful content"],
        reasoning=metric.reason or "",
    )


def evaluate_dimensions(prompt: str) -> list[Dimension]:
    # Preserve original definition order in results despite parallel execution
    order = [name for name, _ in GEVAL_DIMENSIONS]
    futures_map: dict = {}
    with ThreadPoolExecutor(max_workers=len(GEVAL_DIMENSIONS)) as pool:
        for name, criteria in GEVAL_DIMENSIONS:
            futures_map[pool.submit(_run_geval, name, criteria, prompt)] = name
        results: dict[str, Dimension] = {}
        for future in as_completed(futures_map):
            dim = future.result()
            results[dim.name] = dim
    return [results[name] for name in order]


def evaluate_safety(prompt: str) -> list[Dimension]:
    with ThreadPoolExecutor(max_workers=2) as pool:
        bias_future = pool.submit(_run_bias, prompt)
        tox_future = pool.submit(_run_toxicity, prompt)
        return [bias_future.result(), tox_future.result()]


def evaluate_prompt(prompt: str) -> EvaluateResponse:
    # Run quality dimensions and safety metrics in parallel
    with ThreadPoolExecutor(max_workers=2) as pool:
        dims_future = pool.submit(evaluate_dimensions, prompt)
        safety_future = pool.submit(evaluate_safety, prompt)
        return EvaluateResponse(dimensions=dims_future.result() + safety_future.result())
