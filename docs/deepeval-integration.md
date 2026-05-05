# DeepEval Integration

PEF uses [DeepEval](https://github.com/confident-ai/deepeval) 3.9.9 for all evaluation metrics.

## Architecture

```
databricks_client.py  ─── chat_complete()
        │
deepeval_client.py    ─── DatabricksLLM (DeepEvalBaseLLM adapter)
        │
evaluator.py          ─── GEval×6, BiasMetric, ToxicityMetric
stress_tester.py      ─── adversarial attack loop
hallucination.py      ─── HallucinationMetric on sampled output
```

## LLM Adapter

`backend/services/deepeval_client.py` wraps `chat_complete()` in a `DeepEvalBaseLLM` subclass so DeepEval metrics can use the Databricks-hosted model.

```python
class DatabricksLLM(DeepEvalBaseLLM):
    def generate(self, prompt: str) -> str:
        return chat_complete([{"role": "user", "content": prompt}], temperature=0.0)
    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)
```

A singleton is returned by `get_deepeval_model()` to avoid re-instantiation per request.

## Evaluation Dimensions

All scores are normalised to 1–10 integers.

| Dimension | Metric | Direction | Notes |
|-----------|--------|-----------|-------|
| Clarity & Specificity | GEval | higher=better | Chain-of-thought |
| Role / Persona Definition | GEval | higher=better | |
| Output Format Instructions | GEval | higher=better | |
| Context & Background | GEval | higher=better | |
| Constraints & Guardrails | GEval | higher=better | |
| Tone & Style | GEval | higher=better | |
| Bias | BiasMetric | lower=better (inverted) | Score <6 triggers safety warning |
| Toxicity | ToxicityMetric | lower=better (inverted) | Score <6 triggers safety warning |

### Score Normalisation

```python
# GEval (0–1, higher=better)
score = max(1, min(10, round(raw * 9) + 1))

# Bias / Toxicity / Hallucination (0–1, higher=worse → invert)
score = max(1, min(10, round((1 - raw) * 9) + 1))
```

## Split Endpoints

Evaluation is split into two backend calls so the frontend can show step-wise progress:

- `POST /evaluate/dimensions` — runs GEval×6, returns 6 dimensions
- `POST /evaluate/safety` — runs BiasMetric + ToxicityMetric, returns 2 dimensions

The combined `POST /evaluate` merges both.

## Fix Validation

`POST /fix/validate` calls `validate_fix()` in `backend/services/fixer.py`:

1. Re-evaluates the fixed prompt with the full 8-dimension scorecard
2. Compares each dimension score against the original evaluation
3. Returns `regression_warnings` for any dimension that got worse
4. Returns `safety_warnings` for Bias or Toxicity below threshold (score < 6)

## Stress Testing

`POST /stress-test` (`backend/services/stress_tester.py`):

1. Calls the LLM to generate `num_attacks` adversarial inputs targeting the prompt
2. For each attack, calls the LLM again to judge whether the attack succeeded (`PASS`) or was deflected (`FAIL`)
3. Computes `vulnerability_score = round((1 - pass_rate) * 9) + 1` — high = more vulnerable

## Hallucination Check

`POST /hallucination-check` (`backend/services/hallucination.py`):

1. Samples the model's output for the given prompt via `chat_complete`
2. Runs `HallucinationMetric` (requires no ground-truth context — uses model introspection)
3. Inverts the DeepEval score (0–1, higher=more hallucinated) to a 1–10 reliability score

## Configurable Defaults

Five defaults are stored in `config.json` and settable from the Settings page:

| Key | Type | Default |
|-----|------|---------|
| `auto_evaluate_after_fix` | bool | `true` |
| `auto_stress_test` | bool | `false` |
| `auto_hallucination_check` | bool | `false` |
| `stress_test_attack_count` | int | `5` |
| `iterative_fix_passes` | int | `2` |
