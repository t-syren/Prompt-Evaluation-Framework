# PEF — Prompt Evaluation Framework

## What this is
Streamlit + FastAPI app. Streamlit is the UI (frontend/), FastAPI is the backend (backend/).
Tests live in tests/. DeepEval 3.9.9 is used for all metrics.

## Running locally
```bash
# Terminal 1 — backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — frontend
streamlit run frontend/app.py
```

## Python / venv
All commands must use the venv:
```bash
./venv/bin/python
./venv/bin/pytest tests/ -v
./venv/bin/pip install <pkg>
```

## Config
Runtime config in config.json (gitignored). Falls back to .env.
Edit via the Settings page in the UI. Includes 5 evaluation defaults:
- auto_evaluate_after_fix, auto_stress_test, auto_hallucination_check
- stress_test_attack_count, iterative_fix_passes

## LLM
Databricks-hosted Claude via OpenAI-compatible endpoint.
All LLM calls go through backend/services/databricks_client.py.

## DeepEval integration
- Adapter: backend/services/deepeval_client.py (DatabricksLLM wrapping chat_complete)
- Evaluator: backend/services/evaluator.py — GEval×6 + BiasMetric + ToxicityMetric; scores 1–10
- Stress tester: backend/services/stress_tester.py — adversarial attacks via LLM
- Hallucination: backend/services/hallucination.py — HallucinationMetric on sampled output

## Score normalisation
- GEval (0–1, higher=better): round(raw * 9) + 1 clamped [1,10]
- Bias/Toxicity/Hallucination (0–1, higher=worse): round((1-raw) * 9) + 1 clamped [1,10]

## Key routes
- POST /evaluate/dimensions — GEval×6 only
- POST /evaluate/safety — Bias + Toxicity only
- POST /evaluate — full (both)
- POST /fix/generate — multi-pass fix
- POST /fix/validate — regression + safety validation
- POST /stress-test — adversarial stress test
- POST /hallucination-check — hallucination risk

## Tests
```bash
./venv/bin/pytest tests/ -v   # 64 tests
```
