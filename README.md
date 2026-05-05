# Prompt Evaluation Framework (PEF)

AI-powered prompt analysis and improvement tool. Paste any LLM prompt, get a scored evaluation across **8 quality dimensions powered by DeepEval**, and generate an improved version with automatic regression validation, adversarial stress testing, and hallucination risk checks.

## Features

- **8-dimension scoring** — 6 quality dimensions (GEval chain-of-thought) + Bias + Toxicity safety metrics, all rated 1–10
- **AI reasoning** — per-dimension chain-of-thought analysis with specific issues and suggestions
- **Fix with regression guard** — auto-validates that fixed prompts don't score lower on any dimension
- **Safety banners** — warnings when Bias or Toxicity fall below threshold after fixing
- **Stress test** — generate adversarial attacks, judge pass/fail verdicts, compute vulnerability score
- **Hallucination check** — sample the model's output and measure factual reliability
- **Configurable defaults** — toggle auto-checks, set attack count, control iterative fix passes

## Setup

1. Install dependencies (use a virtualenv):
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the backend:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

3. Run the frontend:
   ```bash
   streamlit run frontend/app.py
   ```

4. Open http://localhost:8501 and go to **Settings** to configure your Databricks credentials.

## Configuration

Settings are saved to `config.json` (gitignored) and editable via the Settings page. Falls back to `.env`.

**Connection settings:** Databricks Base URL, LLM Endpoint URL, API Token.

**Evaluation defaults** (configurable in Settings):

| Key | Default | Description |
|-----|---------|-------------|
| `auto_evaluate_after_fix` | `true` | Re-run scorecard after every fix |
| `auto_stress_test` | `false` | Auto-run stress test after evaluation |
| `auto_hallucination_check` | `false` | Auto-run hallucination check after evaluation |
| `stress_test_attack_count` | `5` | Number of adversarial attacks per stress test |
| `iterative_fix_passes` | `2` | Improvement passes per fix run |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/config` | Get current configuration |
| POST | `/config` | Save configuration |
| POST | `/evaluate` | Full evaluation (dimensions + safety) |
| POST | `/evaluate/dimensions` | Quality dimensions only (GEval ×6) |
| POST | `/evaluate/safety` | Safety metrics only (Bias + Toxicity) |
| POST | `/fix` | Generate fixed prompt (single pass) |
| POST | `/fix/generate` | Generate fixed prompt (multi-pass) |
| POST | `/fix/validate` | Validate fix — regression + safety warnings |
| POST | `/refine` | Refine with user feedback |
| POST | `/stress-test` | Adversarial stress test |
| POST | `/hallucination-check` | Hallucination risk check |
| POST | `/export` | Export evaluation report |

## Tests

```bash
./venv/bin/pytest tests/ -v
```

64 tests, all passing.

## Deployment (Databricks Apps)

Deploy `backend/` and `frontend/` as separate Databricks App services. Set `BACKEND_URL` env var in the frontend service to point to the backend service URL.
