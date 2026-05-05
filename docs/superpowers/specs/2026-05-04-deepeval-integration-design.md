# DeepEval Integration — Implementation Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate DeepEval into PEF to replace the single-pass LLM evaluator with G-Eval chain-of-thought scoring, add Bias and Toxicity safety dimensions, improve the fixer with automatic validation, add on-demand Stress Test and Hallucination Risk features, expose per-feature defaults in Settings, and show real step-wise progress for every multi-step operation.

**Architecture:** DeepEval runs entirely on the existing Databricks endpoint via a custom `DeepEvalBaseLLM` adapter — no new credentials. Backend splits into smaller sub-endpoints so the frontend can show real step-by-step progress using `st.status()`. Advanced features (Stress Test, Hallucination Risk) are on-demand buttons that fire only when clicked, or automatically if the user enables them in Settings defaults.

**Tech Stack:** DeepEval (G-Eval, BiasMetric, ToxicityMetric, RedTeamer, HallucinationMetric), FastAPI, Streamlit ≥1.28 (st.status), Pydantic v2, httpx, Databricks OpenAI-compatible endpoint.

---

## 1. Architecture Overview

### New backend files
| File | Responsibility |
|---|---|
| `backend/services/deepeval_client.py` | `DeepEvalBaseLLM` subclass wrapping `chat_complete` from `databricks_client.py`. Reads credentials from `config_manager` at call time. |
| `backend/services/stress_tester.py` | `RedTeamer` wrapper — generates adversarial attacks and scores prompt vulnerability. |
| `backend/services/hallucination.py` | Generates a sample output via Databricks then runs `HallucinationMetric` against it. |
| `backend/routes/advanced.py` | `POST /stress-test`, `POST /hallucination-check` endpoints. |

### Modified backend files
| File | Change |
|---|---|
| `backend/services/evaluator.py` | Replace single LLM call with G-Eval × 6 + BiasMetric + ToxicityMetric. Returns 8 dimensions. Each dimension now carries a `reasoning` field. |
| `backend/services/fixer.py` | Pass G-Eval `reasoning` to fixer prompt. Add iterative retry (max 2 passes) if any dimension scores < 5 after fixing. |
| `backend/routes/evaluate.py` | Split into `POST /evaluate/dimensions` and `POST /evaluate/safety` for step-wise frontend progress. |
| `backend/routes/fix.py` | Split into `POST /fix/generate` and `POST /fix/validate`. |
| `backend/models/schemas.py` | Add `reasoning` to `Dimension`. Add `FixValidateResponse`, `StressTestRequest/Response`, `HallucinationCheckRequest/Response`, `DefaultsConfig`. |
| `backend/services/config_manager.py` | Persist and load new defaults fields alongside Databricks credentials. |
| `backend/main.py` | Register `advanced` router. |

### Modified frontend files
| File | Change |
|---|---|
| `frontend/pages/2_Evaluate_Fix.py` | Step-wise `st.status()` progress for all flows. Advanced feature buttons after scorecard. Regression guard + safety warnings after Evaluate Improvement. |
| `frontend/pages/3_Settings.py` | New "Evaluation Defaults" section with toggles and dropdowns. |
| `frontend/pages/1_Get_Started.py` | Updated to describe 8 dimensions, advanced features, and defaults. |
| `frontend/app.py` | Updated home page description. |

### New docs
| File | Content |
|---|---|
| `README.md` | Full rewrite covering architecture, features, setup, DeepEval integration. |
| `CLAUDE.md` | Updated with new services, routes, and config fields. |
| `docs/deepeval-integration.md` | Technical reference: adapter pattern, metric configuration, score normalisation. |

---

## 2. Core Evaluation — G-Eval + Safety

### DeepEval LLM adapter (`deepeval_client.py`)
Subclasses `DeepEvalBaseLLM`. Implements `generate()` and `a_generate()` by delegating to `chat_complete()` from `databricks_client.py`. Credentials loaded from `config_manager.load()` at call time — no caching, always fresh.

### Updated evaluator (`evaluator.py`)
Runs 8 metrics against the prompt text:

| Metric | DeepEval class | Criteria |
|---|---|---|
| Clarity & Specificity | `GEval` | Is the prompt unambiguous, precise, and specific about what it wants? |
| Role / Persona Definition | `GEval` | Is there a clear role or persona established for the model? |
| Output Format Instructions | `GEval` | Does the prompt specify the desired output format clearly? |
| Context & Background | `GEval` | Is sufficient context provided for the model to complete the task? |
| Constraints & Guardrails | `GEval` | Are limitations, boundaries, and restrictions clearly stated? |
| Tone & Style | `GEval` | Is the desired tone, style, and register specified? |
| Bias | `BiasMetric` | Does the prompt contain political, gender, racial, or other bias? |
| Toxicity | `ToxicityMetric` | Does the prompt contain harmful, offensive, or toxic language? |

**Score normalisation:** G-Eval returns 0–1 float → multiply by 10, round to int, clamp to 1–10. Bias/Toxicity return 0–1 where 1 = maximally bad → score = `round((1 - raw) * 9) + 1`.

**Reasoning field:** G-Eval's `reason` string stored in `Dimension.reasoning`. Shown in scorecard expander detail view. Passed to fixer service for richer context.

### Split endpoints for step-wise progress
```
POST /evaluate/dimensions   body: { prompt }
    → runs G-Eval × 6, returns dimensions[0:6] with reasoning

POST /evaluate/safety       body: { prompt }
    → runs BiasMetric + ToxicityMetric, returns dimensions[6:8]
```

Frontend calls these sequentially, writing each step to `st.status()` as it completes.

---

## 3. Fixer Improvements

### Richer fixer context
`_build_user_message()` in `fixer.py` now includes `reasoning` per dimension:
```
- Clarity & Specificity (score 4/10): reasoning: "The prompt does not specify..."
  issues: [...], suggestions: [...]
```

### Split fix endpoints
```
POST /fix/generate    body: { prompt, evaluation, mode }
    → returns { fixed_prompt } or { variants }

POST /fix/validate    body: { original_prompt, fixed_prompt, original_evaluation }
    → runs G-Eval × 6 + Bias + Toxicity on fixed_prompt
    → returns { post_eval, regression_warnings, safety_warnings }
```

`regression_warnings`: list of `{ dimension, original_score, fixed_score }` where `fixed_score < original_score`.
`safety_warnings`: list of dimension names where Bias or Toxicity score < 6.

### Iterative auto-retry (single mode only)
After `POST /fix/generate`, the backend checks if any G-Eval dimension still scores < 5. If so, runs a second fix pass with a targeted system prompt listing only the failing dimensions and their G-Eval reasoning. Max 2 passes. Frontend sees only the final (better) result.

### "📊 Evaluate Improvement" button
Kept as on-demand. Clicking it calls `POST /fix/validate` on the current fixed prompt text. Step-wise progress shown via `st.status()`. Regression guard warning and safety badges rendered after completion. Button disappears once validation has run (replaced by comparison table).

---

## 4. Advanced Features

### Stress Test (`POST /stress-test`)
```
Request:  { prompt, num_attacks: int }
Response: { attacks: [{ input, attack_type, verdict, reason }], vulnerability_score: int (1-10) }
```
Uses DeepEval `RedTeamer`. Attack types include: prompt injection, jailbreak, roleplay manipulation, goal hijacking. `vulnerability_score` = `round((1 - pass_rate) * 9) + 1`.

UI: "🔴 Run Stress Test" button below scorecard. Step-wise progress: "Generating attack variants…" → "Testing attack 1/N…" → "Scoring vulnerability…". Results shown as a table with attack type badges and pass/fail indicators.

### Hallucination Risk (`POST /hallucination-check`)
```
Request:  { prompt }
Response: { sample_output: str, hallucination_score: int (1-10), verdict: str, reason: str }
```
Step 1: call `chat_complete` with the prompt to generate a sample output. Step 2: run DeepEval `HallucinationMetric` on `(prompt, sample_output)`. Score normalised to 1–10 where 10 = no hallucination risk.

UI: "🧠 Check Hallucination Risk" button below scorecard. Step-wise progress: "Generating sample output…" → "Analysing hallucination risk…". Result: risk score badge + sample output in a collapsed expander + reason text.

---

## 5. Settings Defaults

### New config fields (persisted in `config.json`)
```json
{
  "databricks_base_url": "...",
  "llm_endpoint_url": "...",
  "api_token": "...",
  "auto_evaluate_after_fix": true,
  "auto_stress_test": false,
  "auto_hallucination_check": false,
  "stress_test_attack_count": 5,
  "iterative_fix_passes": 2
}
```

### Settings page — new "Evaluation Defaults" card
```
[✓] Auto-evaluate improvement after fixing
[ ] Auto-run Stress Test after every evaluation
[ ] Auto-run Hallucination Check after every evaluation

Stress Test attack count   [5 ▼]  options: 3, 5, 10
Iterative fix retry passes [2 ▼]  options: 1, 2, 3
```

`ConfigModel` and `ConfigResponse` schemas updated with optional fields (all default to the values above). `config_manager.save()` and `config_manager.load()` updated to handle new fields with fallback defaults so existing `config.json` files without these fields continue to work.

Frontend reads defaults on page load via `GET /config` and pre-populates the toggles. When auto-features are enabled, the corresponding buttons on Evaluate & Fix are skipped — flows trigger automatically with step-wise progress.

---

## 6. Step-wise Progress Pattern

All multi-step flows use `st.status()`:

```python
with st.status("Analysing prompt...", expanded=True) as status:
    st.write("⏳ Running G-Eval — Clarity & Specificity...")
    dims_result = call_evaluate_dimensions(prompt)
    for d in dims_result:
        st.write(f"✅ G-Eval — {d['name']} ({d['score']}/10)")
    st.write("⏳ Checking Bias & Toxicity...")
    safety_result = call_evaluate_safety(prompt)
    for d in safety_result:
        st.write(f"✅ {d['name']} ({d['score']}/10)")
    status.update(label="✅ Analysis complete — 8 dimensions scored", state="complete", expanded=False)
```

| Flow | Steps |
|---|---|
| Analyze | G-Eval ×6 (one write per dimension) → Bias → Toxicity |
| Fix (single) | Generating improved prompt → Iterative retry if needed → Validate G-Eval ×6 → Safety check → Regression check |
| Fix (variants) | Generating 3 variants → Validating each → Safety checks |
| Regenerate with feedback | Applying feedback → Validating → Safety check |
| Stress Test | Generating attacks → Testing each attack → Scoring vulnerability |
| Hallucination Check | Generating sample output → Analysing hallucination risk |

---

## 7. UI Updates Summary

- **Scorecard:** 8 dimension cards (6 G-Eval + Bias + Toxicity). Bias/Toxicity cards use inverted colour scale. Each expander shows G-Eval `reasoning` text.
- **Regression warnings:** Yellow banner above fixed prompt listing any dimensions that scored lower after fixing.
- **Safety badges:** Red badge on fixed prompt card if Bias or Toxicity < 6.
- **Advanced buttons:** "🔴 Run Stress Test" and "🧠 Check Hallucination Risk" appear below the scorecard, hidden if auto-run is enabled in defaults.
- **Get Started page:** Updated step-by-step guide covering 8 dimensions, advanced features, and defaults configuration.
- **Home page:** Updated capability description.

---

## 8. Docs Updates

- **`README.md`:** Full rewrite — what PEF does, architecture diagram (text), setup instructions, feature list, DeepEval integration note.
- **`CLAUDE.md`:** Add new services (`deepeval_client`, `stress_tester`, `hallucination`), new routes (`/evaluate/dimensions`, `/evaluate/safety`, `/fix/generate`, `/fix/validate`, `/stress-test`, `/hallucination-check`), new config fields.
- **`docs/deepeval-integration.md`:** Adapter pattern explanation, G-Eval criteria definitions, score normalisation formulas, how to add a new DeepEval metric.
