import json
from backend.services.databricks_client import chat_complete
from backend.services.evaluator import evaluate_prompt
from backend.models.schemas import (
    EvaluateResponse, FixResponse, FixValidateResponse, RegressionWarning
)

SINGLE_SYSTEM_PROMPT = """You are an expert prompt engineer. Rewrite the given prompt to address all identified issues.

Rules:
- Preserve the original intent completely
- Apply all suggestions, paying close attention to the detailed reasoning provided
- Return ONLY the improved prompt text — no explanation, no preamble, no markdown code fences"""

VARIANTS_SYSTEM_PROMPT = """You are an expert prompt engineer. Rewrite the given prompt in exactly 3 different improved variants.

Rules:
- Each variant must preserve the original intent
- Each variant should apply the evaluation suggestions differently
- Return ONLY a valid JSON array of exactly 3 strings: ["variant1", "variant2", "variant3"]
- No extra text outside the JSON array"""

REFINE_SYSTEM_PROMPT = """You are an expert prompt engineer. You have already improved a prompt once. The user has provided additional feedback.

Rules:
- Apply the user's specific feedback precisely
- Keep all previously applied improvements that the feedback doesn't contradict
- Preserve the original intent throughout
- Return ONLY the refined prompt text — no explanation, no preamble, no markdown code fences"""


def _build_user_message(prompt: str, evaluation: EvaluateResponse) -> str:
    lines = [f"Original prompt:\n{prompt}\n\nEvaluation results:"]
    for d in evaluation.dimensions:
        lines.append(
            f"- {d.name} (score {d.score}/10)\n"
            f"  Reasoning: {d.reasoning or 'N/A'}\n"
            f"  Issues: {d.issues}\n"
            f"  Suggestions: {d.suggestions}"
        )
    return "\n".join(lines)


def fix_prompt(prompt: str, evaluation: EvaluateResponse, mode: str) -> FixResponse:
    user_msg = _build_user_message(prompt, evaluation)

    if mode == "single":
        messages = [
            {"role": "system", "content": SINGLE_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
        fixed = chat_complete(messages, temperature=0.3)
        return FixResponse(fixed_prompt=fixed.strip())

    messages = [
        {"role": "system", "content": VARIANTS_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]
    for attempt in range(2):
        raw = chat_complete(messages, temperature=0.7)
        try:
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            variants = json.loads(raw)
            if not isinstance(variants, list) or len(variants) != 3:
                raise ValueError("Expected list of 3 variants")
            return FixResponse(variants=variants)
        except Exception:
            if attempt == 1:
                raise ValueError("Failed to parse variants response after 2 attempts.")
    raise ValueError("Unreachable")


def refine_prompt(original: str, current_fixed: str, evaluation: EvaluateResponse, feedback: str, mode: str) -> FixResponse:
    eval_summary = "\n".join(
        f"- {d.name} (score {d.score}/10): reasoning: {d.reasoning or 'N/A'}, issues: {d.issues}, suggestions: {d.suggestions}"
        for d in evaluation.dimensions
    )
    user_msg = (
        f"Original prompt:\n{original}\n\n"
        f"Evaluation results:\n{eval_summary}\n\n"
        f"Previously improved prompt:\n{current_fixed}\n\n"
        f"User feedback:\n{feedback}"
    )

    if mode == "single":
        messages = [
            {"role": "system", "content": REFINE_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
        refined = chat_complete(messages, temperature=0.3)
        return FixResponse(fixed_prompt=refined.strip())

    variants_refine = REFINE_SYSTEM_PROMPT + "\n\nReturn ONLY a valid JSON array of exactly 3 refined strings."
    messages = [
        {"role": "system", "content": variants_refine},
        {"role": "user", "content": user_msg},
    ]
    for attempt in range(2):
        raw = chat_complete(messages, temperature=0.7)
        try:
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            variants = json.loads(raw)
            if not isinstance(variants, list) or len(variants) != 3:
                raise ValueError("Expected list of 3 variants")
            return FixResponse(variants=variants)
        except Exception:
            if attempt == 1:
                raise ValueError("Failed to parse variants response after 2 attempts.")
    raise ValueError("Unreachable")


def validate_fix(original_prompt: str, fixed_prompt: str, original_evaluation: EvaluateResponse) -> FixValidateResponse:
    post_eval = evaluate_prompt(fixed_prompt)

    orig_scores = {d.name: d.score for d in original_evaluation.dimensions}
    regression_warnings = [
        RegressionWarning(
            dimension=d.name,
            original_score=orig_scores[d.name],
            fixed_score=d.score,
        )
        for d in post_eval.dimensions
        if d.name in orig_scores and d.score < orig_scores[d.name]
    ]

    safety_warnings = [
        d.name for d in post_eval.dimensions
        if d.name in ("Bias", "Toxicity") and d.score < 6
    ]

    return FixValidateResponse(
        post_eval=post_eval,
        regression_warnings=regression_warnings,
        safety_warnings=safety_warnings,
    )
