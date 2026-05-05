# Prompt Evaluation Framework (PEF) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Streamlit + FastAPI prompt evaluation and improvement tool powered by a Databricks-hosted Claude LLM.

**Architecture:** Streamlit UI (3 pages) calls a FastAPI backend via HTTP. FastAPI handles all LLM interactions using the OpenAI-compatible Databricks serving endpoint. Runtime config (Databricks URL, LLM endpoint, PAT token) is stored in `config.json` and editable via the Settings page.

**Tech Stack:** Python 3.10+, Streamlit, FastAPI, Uvicorn, OpenAI SDK (pointed at Databricks), Pydantic v2, httpx, python-dotenv, pytest

---

## File Map

```
PEF/
├── backend/
│   ├── main.py                        # FastAPI app + router registration
│   ├── models/
│   │   └── schemas.py                 # All Pydantic request/response models
│   ├── services/
│   │   ├── config_manager.py          # Read/write config.json, .env fallback
│   │   ├── databricks_client.py       # OpenAI SDK wrapper for Databricks LLM
│   │   ├── evaluator.py               # Evaluation prompt logic + response parsing
│   │   └── fixer.py                   # Fix prompt logic + response parsing
│   └── routes/
│       ├── evaluate.py                # POST /evaluate
│       ├── fix.py                     # POST /fix
│       ├── export.py                  # POST /export
│       └── config.py                  # GET/POST /config
├── frontend/
│   ├── app.py                         # Streamlit entry point + sidebar nav
│   └── pages/
│       ├── 1_Get_Started.py           # Docs / how-to page
│       ├── 2_Evaluate_Fix.py          # Main tool page
│       └── 3_Settings.py             # Databricks config page
├── tests/
│   ├── conftest.py                    # Shared fixtures
│   ├── test_config_manager.py
│   ├── test_evaluator.py
│   ├── test_fixer.py
│   ├── test_routes_evaluate.py
│   ├── test_routes_fix.py
│   └── test_routes_export.py
├── config.json                        # Runtime config (gitignored)
├── .env                               # Fallback config (gitignored)
├── .env.example                       # Template (committed)
├── .gitignore
├── requirements.txt
├── README.md
└── CLAUDE.md
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `CLAUDE.md`
- Create: `README.md`
- Create: `backend/__init__.py`, `backend/models/__init__.py`, `backend/services/__init__.py`, `backend/routes/__init__.py`
- Create: `frontend/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p backend/models backend/services backend/routes
mkdir -p frontend/pages
mkdir -p tests
touch backend/__init__.py backend/models/__init__.py backend/services/__init__.py backend/routes/__init__.py
touch frontend/__init__.py
touch tests/__init__.py
```

- [ ] **Step 2: Create `requirements.txt`**

```
fastapi==0.115.5
uvicorn==0.32.1
streamlit==1.40.1
httpx==0.28.0
openai==1.55.3
pydantic==2.10.2
python-dotenv==1.0.1
pytest==8.3.4
pytest-asyncio==0.24.0
```

- [ ] **Step 3: Create `.gitignore`**

```
config.json
.env
__pycache__/
*.pyc
.pytest_cache/
.venv/
dist/
*.egg-info/
```

- [ ] **Step 4: Create `.env.example`**

```
DATABRICKS_BASE_URL=https://<workspace>.azuredatabricks.net
LLM_ENDPOINT_URL=https://<workspace>.azuredatabricks.net/serving-endpoints/<model>/invocations
DATABRICKS_TOKEN=dapi...
BACKEND_URL=http://localhost:8000
```

- [ ] **Step 5: Create `CLAUDE.md`**

```markdown
# PEF — Prompt Evaluation Framework

## What this is
Streamlit + FastAPI app. Streamlit is the UI (frontend/), FastAPI is the backend (backend/).
Tests live in tests/.

## Running locally
```bash
# Terminal 1 — backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend && streamlit run app.py
```

## Config
Runtime config in config.json (gitignored). Falls back to .env.
Edit via the Settings page in the UI.

## LLM
Databricks-hosted Claude via OpenAI-compatible endpoint.
All LLM calls go through backend/services/databricks_client.py.

## Tests
pytest tests/ -v
```

- [ ] **Step 6: Create `README.md`**

```markdown
# Prompt Evaluation Framework (PEF)

AI-powered prompt analysis and improvement tool. Paste any LLM prompt, get a scored evaluation across 6 dimensions, and generate an improved version with one click.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your Databricks credentials:
   ```bash
   cp .env.example .env
   ```

3. Run the backend:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

4. Run the frontend:
   ```bash
   streamlit run frontend/app.py
   ```

5. Open http://localhost:8501 in your browser.

## Configuration

Go to the **Settings** page in the UI to configure your Databricks endpoint, LLM URL, and token. Settings are saved to `config.json`.

## Deployment (Databricks Apps)

Deploy `backend/` and `frontend/` as separate Databricks App services. Set `BACKEND_URL` env var in the frontend service to point to the backend service URL.
```

- [ ] **Step 7: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: All packages install without errors.

- [ ] **Step 8: Commit scaffold**

```bash
git init
git add requirements.txt .gitignore .env.example CLAUDE.md README.md backend/ frontend/ tests/
git commit -m "feat: project scaffold for PEF"
```

---

## Task 2: Pydantic Schemas

**Files:**
- Create: `backend/models/schemas.py`
- Test: `tests/test_schemas.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_schemas.py`:

```python
import pytest
from backend.models.schemas import (
    EvaluatRequest,
    Dimension,
    EvaluateResponse,
    FixRequest,
    FixResponse,
    ExportRequest,
    ConfigModel,
    ConfigResponse,
)


def test_evaluate_request_valid():
    req = EvaluatRequest(prompt="Tell me a joke")
    assert req.prompt == "Tell me a joke"


def test_evaluate_request_empty_prompt_fails():
    with pytest.raises(Exception):
        EvaluatRequest(prompt="")


def test_dimension_valid():
    d = Dimension(
        name="Clarity",
        score=7,
        issues=["Too vague"],
        suggestions=["Be more specific"],
    )
    assert d.score == 7


def test_dimension_score_out_of_range():
    with pytest.raises(Exception):
        Dimension(name="Clarity", score=11, issues=[], suggestions=[])


def test_evaluate_response_valid():
    resp = EvaluateResponse(
        dimensions=[
            Dimension(name="Clarity", score=8, issues=[], suggestions=[])
        ]
    )
    assert len(resp.dimensions) == 1


def test_fix_request_single_mode():
    req = FixRequest(
        prompt="Write code",
        evaluation=EvaluateResponse(dimensions=[]),
        mode="single",
    )
    assert req.mode == "single"


def test_fix_request_invalid_mode():
    with pytest.raises(Exception):
        FixRequest(
            prompt="Write code",
            evaluation=EvaluateResponse(dimensions=[]),
            mode="invalid",
        )


def test_fix_response_single():
    resp = FixResponse(fixed_prompt="Improved prompt")
    assert resp.fixed_prompt == "Improved prompt"
    assert resp.variants is None


def test_fix_response_variants():
    resp = FixResponse(variants=["v1", "v2", "v3"])
    assert len(resp.variants) == 3
    assert resp.fixed_prompt is None


def test_config_model_valid():
    cfg = ConfigModel(
        databricks_base_url="https://example.com",
        llm_endpoint_url="https://example.com/invocations",
        api_token="dapi123",
    )
    assert cfg.api_token == "dapi123"


def test_config_response_masks_token():
    resp = ConfigResponse(
        databricks_base_url="https://example.com",
        llm_endpoint_url="https://example.com/invocations",
        api_token_set=True,
    )
    assert resp.api_token_set is True
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_schemas.py -v
```

Expected: ImportError — `backend.models.schemas` does not exist yet.

- [ ] **Step 3: Implement `backend/models/schemas.py`**

```python
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class EvaluatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class Dimension(BaseModel):
    name: str
    score: int = Field(..., ge=1, le=10)
    issues: list[str]
    suggestions: list[str]


class EvaluateResponse(BaseModel):
    dimensions: list[Dimension]


class FixRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    evaluation: EvaluateResponse
    mode: Literal["single", "variants"]


class FixResponse(BaseModel):
    fixed_prompt: Optional[str] = None
    variants: Optional[list[str]] = None


class ExportRequest(BaseModel):
    original_prompt: str
    evaluation: EvaluateResponse
    fixed_prompt: Optional[str] = None
    variants: Optional[list[str]] = None
    mode: Literal["single", "variants"] = "single"


class ConfigModel(BaseModel):
    databricks_base_url: str
    llm_endpoint_url: str
    api_token: str


class ConfigResponse(BaseModel):
    databricks_base_url: str
    llm_endpoint_url: str
    api_token_set: bool
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_schemas.py -v
```

Expected: All 12 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/models/schemas.py tests/test_schemas.py
git commit -m "feat: add Pydantic schemas for all PEF request/response models"
```

---

## Task 3: Config Manager

**Files:**
- Create: `backend/services/config_manager.py`
- Test: `tests/test_config_manager.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_config_manager.py`:

```python
import json
import os
import pytest
from unittest.mock import patch
from backend.services.config_manager import ConfigManager


def test_load_from_config_json(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps({
        "databricks_base_url": "https://db.example.com",
        "llm_endpoint_url": "https://db.example.com/invocations",
        "api_token": "dapi_test"
    }))
    manager = ConfigManager(config_path=str(cfg_file))
    cfg = manager.load()
    assert cfg["api_token"] == "dapi_test"
    assert cfg["databricks_base_url"] == "https://db.example.com"


def test_load_falls_back_to_env(tmp_path):
    cfg_file = tmp_path / "config.json"  # does not exist
    env_vars = {
        "DATABRICKS_BASE_URL": "https://env.example.com",
        "LLM_ENDPOINT_URL": "https://env.example.com/invocations",
        "DATABRICKS_TOKEN": "dapi_env",
    }
    with patch.dict(os.environ, env_vars):
        manager = ConfigManager(config_path=str(cfg_file))
        cfg = manager.load()
    assert cfg["api_token"] == "dapi_env"
    assert cfg["databricks_base_url"] == "https://env.example.com"


def test_save_writes_config_json(tmp_path):
    cfg_file = tmp_path / "config.json"
    manager = ConfigManager(config_path=str(cfg_file))
    manager.save({
        "databricks_base_url": "https://new.example.com",
        "llm_endpoint_url": "https://new.example.com/invocations",
        "api_token": "dapi_new"
    })
    saved = json.loads(cfg_file.read_text())
    assert saved["api_token"] == "dapi_new"


def test_load_raises_when_no_config_and_no_env(tmp_path):
    cfg_file = tmp_path / "config.json"
    with patch.dict(os.environ, {}, clear=True):
        manager = ConfigManager(config_path=str(cfg_file))
        with pytest.raises(ValueError, match="No configuration found"):
            manager.load()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_config_manager.py -v
```

Expected: ImportError — module does not exist yet.

- [ ] **Step 3: Implement `backend/services/config_manager.py`**

```python
import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.json"


class ConfigManager:
    def __init__(self, config_path: str = str(CONFIG_PATH)):
        self.config_path = Path(config_path)

    def load(self) -> dict:
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)

        base_url = os.getenv("DATABRICKS_BASE_URL")
        llm_url = os.getenv("LLM_ENDPOINT_URL")
        token = os.getenv("DATABRICKS_TOKEN")

        if not all([base_url, llm_url, token]):
            raise ValueError(
                "No configuration found. Please configure credentials in the Settings page."
            )

        return {
            "databricks_base_url": base_url,
            "llm_endpoint_url": llm_url,
            "api_token": token,
        }

    def save(self, config: dict) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)


config_manager = ConfigManager()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_config_manager.py -v
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/services/config_manager.py tests/test_config_manager.py
git commit -m "feat: add ConfigManager with config.json read/write and .env fallback"
```

---

## Task 4: Databricks Client

**Files:**
- Create: `backend/services/databricks_client.py`
- Test: (integration-style, mocked — tested via evaluator/fixer tests in Tasks 5–6)

- [ ] **Step 1: Implement `backend/services/databricks_client.py`**

```python
from openai import OpenAI
from backend.services.config_manager import config_manager


def get_llm_client() -> tuple[OpenAI, str]:
    """Returns (OpenAI client, model_name) configured for Databricks."""
    cfg = config_manager.load()
    llm_url = cfg["llm_endpoint_url"]
    token = cfg["api_token"]

    # Strip /invocations suffix — openai SDK appends /chat/completions
    base_url = llm_url.replace("/invocations", "")
    # Extract model name from endpoint path
    model_name = base_url.rstrip("/").split("/")[-1]
    # Set base_url to parent (serving-endpoints level)
    serving_base = base_url.rsplit("/", 1)[0] + "/"

    client = OpenAI(api_key=token, base_url=serving_base)
    return client, model_name


def chat_complete(messages: list[dict], temperature: float = 0.2) -> str:
    """Call the Databricks LLM and return the response text."""
    client, model_name = get_llm_client()
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
```

- [ ] **Step 2: Commit**

```bash
git add backend/services/databricks_client.py
git commit -m "feat: add Databricks LLM client wrapper using OpenAI SDK"
```

---

## Task 5: Evaluator Service

**Files:**
- Create: `backend/services/evaluator.py`
- Test: `tests/test_evaluator.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_evaluator.py`:

```python
import json
import pytest
from unittest.mock import patch
from backend.services.evaluator import evaluate_prompt
from backend.models.schemas import EvaluateResponse


MOCK_LLM_RESPONSE = json.dumps({
    "dimensions": [
        {
            "name": "Clarity & Specificity",
            "score": 6,
            "issues": ["The objective is vague"],
            "suggestions": ["State clearly what output format you expect"]
        },
        {
            "name": "Role / Persona Definition",
            "score": 3,
            "issues": ["No role defined"],
            "suggestions": ["Add a system role like 'You are an expert in...'"]
        },
        {
            "name": "Output Format Instructions",
            "score": 5,
            "issues": ["No format specified"],
            "suggestions": ["Specify JSON, markdown, or plain text output"]
        },
        {
            "name": "Context & Background",
            "score": 4,
            "issues": ["Missing context"],
            "suggestions": ["Provide relevant background information"]
        },
        {
            "name": "Constraints & Guardrails",
            "score": 7,
            "issues": [],
            "suggestions": ["Consider adding length constraints"]
        },
        {
            "name": "Tone & Style",
            "score": 6,
            "issues": ["Tone not specified"],
            "suggestions": ["Specify formal or informal tone"]
        }
    ]
})


def test_evaluate_prompt_returns_evaluation():
    with patch("backend.services.evaluator.chat_complete", return_value=MOCK_LLM_RESPONSE):
        result = evaluate_prompt("Write me a summary of this document.")
    assert isinstance(result, EvaluateResponse)
    assert len(result.dimensions) == 6
    assert result.dimensions[0].name == "Clarity & Specificity"
    assert result.dimensions[0].score == 6


def test_evaluate_prompt_all_scores_in_range():
    with patch("backend.services.evaluator.chat_complete", return_value=MOCK_LLM_RESPONSE):
        result = evaluate_prompt("Any prompt")
    for dim in result.dimensions:
        assert 1 <= dim.score <= 10


def test_evaluate_prompt_retries_on_bad_json():
    bad_json = "not valid json"
    good_json = MOCK_LLM_RESPONSE
    call_count = {"n": 0}

    def mock_chat(messages, temperature=0.2):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return bad_json
        return good_json

    with patch("backend.services.evaluator.chat_complete", side_effect=mock_chat):
        result = evaluate_prompt("A prompt")
    assert call_count["n"] == 2
    assert isinstance(result, EvaluateResponse)


def test_evaluate_prompt_raises_after_two_bad_responses():
    with patch("backend.services.evaluator.chat_complete", return_value="not json"):
        with pytest.raises(ValueError, match="Failed to parse evaluation"):
            evaluate_prompt("A prompt")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_evaluator.py -v
```

Expected: ImportError — module does not exist.

- [ ] **Step 3: Implement `backend/services/evaluator.py`**

```python
import json
from backend.services.databricks_client import chat_complete
from backend.models.schemas import EvaluateResponse

SYSTEM_PROMPT = """You are an expert prompt engineer. Analyze the following LLM prompt and evaluate it across exactly these 6 dimensions:

1. Clarity & Specificity
2. Role / Persona Definition
3. Output Format Instructions
4. Context & Background
5. Constraints & Guardrails
6. Tone & Style

For each dimension provide:
- score: integer from 1 to 10 (10 = excellent)
- issues: list of specific problems found (empty list if none)
- suggestions: list of actionable improvements (empty list if none)

Return ONLY a valid JSON object with this exact structure:
{
  "dimensions": [
    {
      "name": "Clarity & Specificity",
      "score": 7,
      "issues": ["issue text"],
      "suggestions": ["suggestion text"]
    }
  ]
}

Include all 6 dimensions in the response, in the order listed above. No extra text outside the JSON."""


def _parse_response(text: str) -> EvaluateResponse:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    data = json.loads(text)
    return EvaluateResponse(**data)


def evaluate_prompt(prompt: str) -> EvaluateResponse:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Evaluate this prompt:\n\n{prompt}"},
    ]
    for attempt in range(2):
        raw = chat_complete(messages, temperature=0.1)
        try:
            return _parse_response(raw)
        except (json.JSONDecodeError, Exception):
            if attempt == 1:
                raise ValueError(f"Failed to parse evaluation response after 2 attempts.")
    raise ValueError("Failed to parse evaluation response after 2 attempts.")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_evaluator.py -v
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/services/evaluator.py tests/test_evaluator.py
git commit -m "feat: add evaluator service with 6-dimension LLM scoring"
```

---

## Task 6: Fixer Service

**Files:**
- Create: `backend/services/fixer.py`
- Test: `tests/test_fixer.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_fixer.py`:

```python
import json
import pytest
from unittest.mock import patch
from backend.services.fixer import fix_prompt
from backend.models.schemas import EvaluateResponse, Dimension, FixResponse

SAMPLE_EVALUATION = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=5, issues=["Too vague"], suggestions=["Be specific"]),
    Dimension(name="Role / Persona Definition", score=3, issues=["No role"], suggestions=["Add a role"]),
    Dimension(name="Output Format Instructions", score=4, issues=["No format"], suggestions=["Add format"]),
    Dimension(name="Context & Background", score=6, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=7, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=5, issues=["Tone unclear"], suggestions=["Specify tone"]),
])


def test_fix_single_mode_returns_fixed_prompt():
    with patch("backend.services.fixer.chat_complete", return_value="You are a helpful assistant. Summarize the document in 3 bullet points."):
        result = fix_prompt("Summarize this.", SAMPLE_EVALUATION, mode="single")
    assert isinstance(result, FixResponse)
    assert result.fixed_prompt is not None
    assert result.variants is None


def test_fix_variants_mode_returns_three_variants():
    mock_variants = json.dumps([
        "Variant 1: improved prompt",
        "Variant 2: improved prompt",
        "Variant 3: improved prompt"
    ])
    with patch("backend.services.fixer.chat_complete", return_value=mock_variants):
        result = fix_prompt("Summarize this.", SAMPLE_EVALUATION, mode="variants")
    assert result.variants is not None
    assert len(result.variants) == 3
    assert result.fixed_prompt is None


def test_fix_variants_retries_on_bad_json():
    bad = "not json"
    good = json.dumps(["v1", "v2", "v3"])
    call_count = {"n": 0}

    def mock_chat(messages, temperature=0.2):
        call_count["n"] += 1
        return bad if call_count["n"] == 1 else good

    with patch("backend.services.fixer.chat_complete", side_effect=mock_chat):
        result = fix_prompt("prompt", SAMPLE_EVALUATION, mode="variants")
    assert call_count["n"] == 2
    assert len(result.variants) == 3


def test_fix_variants_raises_after_two_bad_responses():
    with patch("backend.services.fixer.chat_complete", return_value="not json"):
        with pytest.raises(ValueError, match="Failed to parse"):
            fix_prompt("prompt", SAMPLE_EVALUATION, mode="variants")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_fixer.py -v
```

Expected: ImportError — module does not exist.

- [ ] **Step 3: Implement `backend/services/fixer.py`**

```python
import json
from backend.services.databricks_client import chat_complete
from backend.models.schemas import EvaluateResponse, FixResponse

SINGLE_SYSTEM_PROMPT = """You are an expert prompt engineer. Rewrite the given prompt to address all identified issues and implement all suggestions from the evaluation.

Rules:
- Preserve the original intent completely
- Apply all suggested improvements
- Return ONLY the improved prompt text — no explanation, no preamble, no markdown code fences"""

VARIANTS_SYSTEM_PROMPT = """You are an expert prompt engineer. Rewrite the given prompt in exactly 3 different improved variants, each taking a slightly different approach to address the evaluation issues.

Rules:
- Each variant must preserve the original intent
- Each variant should apply the evaluation suggestions differently
- Return ONLY a valid JSON array of exactly 3 strings: ["variant1", "variant2", "variant3"]
- No extra text outside the JSON array"""


def _build_user_message(prompt: str, evaluation: EvaluateResponse) -> str:
    eval_summary = "\n".join(
        f"- {d.name} (score {d.score}/10): issues: {d.issues}, suggestions: {d.suggestions}"
        for d in evaluation.dimensions
    )
    return f"Original prompt:\n{prompt}\n\nEvaluation results:\n{eval_summary}"


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
    raise ValueError("Failed to parse variants response after 2 attempts.")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_fixer.py -v
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/services/fixer.py tests/test_fixer.py
git commit -m "feat: add fixer service with single and 3-variant prompt improvement modes"
```

---

## Task 7: FastAPI Routes — Config

**Files:**
- Create: `backend/routes/config.py`
- Test: `tests/test_routes_config.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_routes_config.py`:

```python
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


def test_get_config_returns_masked_token():
    mock_cfg = {
        "databricks_base_url": "https://db.example.com",
        "llm_endpoint_url": "https://db.example.com/invocations",
        "api_token": "dapi_secret",
    }
    with patch("backend.routes.config.config_manager") as mock_mgr:
        mock_mgr.load.return_value = mock_cfg
        from backend.main import app
        client = TestClient(app)
        response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert data["api_token_set"] is True
    assert "dapi_secret" not in str(data)
    assert data["databricks_base_url"] == "https://db.example.com"


def test_post_config_saves_and_returns_success():
    payload = {
        "databricks_base_url": "https://new.example.com",
        "llm_endpoint_url": "https://new.example.com/invocations",
        "api_token": "dapi_new",
    }
    with patch("backend.routes.config.config_manager") as mock_mgr:
        mock_mgr.save.return_value = None
        from backend.main import app
        client = TestClient(app)
        response = client.post("/config", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "saved"
    mock_mgr.save.assert_called_once()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_routes_config.py -v
```

Expected: ImportError or 404 — routes not wired yet.

- [ ] **Step 3: Implement `backend/routes/config.py`**

```python
from fastapi import APIRouter, HTTPException
from backend.models.schemas import ConfigModel, ConfigResponse
from backend.services.config_manager import config_manager

router = APIRouter()


@router.get("/config", response_model=ConfigResponse)
def get_config():
    try:
        cfg = config_manager.load()
    except ValueError:
        return ConfigResponse(
            databricks_base_url="",
            llm_endpoint_url="",
            api_token_set=False,
        )
    return ConfigResponse(
        databricks_base_url=cfg["databricks_base_url"],
        llm_endpoint_url=cfg["llm_endpoint_url"],
        api_token_set=bool(cfg.get("api_token")),
    )


@router.post("/config")
def save_config(payload: ConfigModel):
    config_manager.save({
        "databricks_base_url": payload.databricks_base_url,
        "llm_endpoint_url": payload.llm_endpoint_url,
        "api_token": payload.api_token,
    })
    return {"status": "saved"}
```

- [ ] **Step 4: Create `backend/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import config, evaluate, fix, export

app = FastAPI(title="PEF API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config.router)
app.include_router(evaluate.router)
app.include_router(fix.router)
app.include_router(export.router)
```

Also create stub files for the remaining routes so imports don't fail:

`backend/routes/evaluate.py`:
```python
from fastapi import APIRouter
router = APIRouter()
```

`backend/routes/fix.py`:
```python
from fastapi import APIRouter
router = APIRouter()
```

`backend/routes/export.py`:
```python
from fastapi import APIRouter
router = APIRouter()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_routes_config.py -v
```

Expected: All 2 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/main.py backend/routes/config.py backend/routes/evaluate.py backend/routes/fix.py backend/routes/export.py tests/test_routes_config.py
git commit -m "feat: add FastAPI app + config GET/POST routes"
```

---

## Task 8: FastAPI Routes — Evaluate & Fix

**Files:**
- Modify: `backend/routes/evaluate.py`
- Modify: `backend/routes/fix.py`
- Test: `tests/test_routes_evaluate.py`, `tests/test_routes_fix.py`

- [ ] **Step 1: Write failing tests for evaluate route**

Create `tests/test_routes_evaluate.py`:

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.models.schemas import EvaluateResponse, Dimension
from backend.main import app

client = TestClient(app)

MOCK_EVAL = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=7, issues=[], suggestions=["Be more specific"]),
    Dimension(name="Role / Persona Definition", score=5, issues=["No role"], suggestions=["Add role"]),
    Dimension(name="Output Format Instructions", score=6, issues=[], suggestions=[]),
    Dimension(name="Context & Background", score=8, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=9, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=7, issues=[], suggestions=[]),
])


def test_evaluate_returns_200_with_dimensions():
    with patch("backend.routes.evaluate.evaluate_prompt", return_value=MOCK_EVAL):
        response = client.post("/evaluate", json={"prompt": "Write a summary"})
    assert response.status_code == 200
    data = response.json()
    assert "dimensions" in data
    assert len(data["dimensions"]) == 6


def test_evaluate_empty_prompt_returns_422():
    response = client.post("/evaluate", json={"prompt": ""})
    assert response.status_code == 422


def test_evaluate_missing_prompt_returns_422():
    response = client.post("/evaluate", json={})
    assert response.status_code == 422


def test_evaluate_llm_error_returns_503():
    with patch("backend.routes.evaluate.evaluate_prompt", side_effect=Exception("LLM unreachable")):
        response = client.post("/evaluate", json={"prompt": "Some prompt"})
    assert response.status_code == 503
```

- [ ] **Step 2: Write failing tests for fix route**

Create `tests/test_routes_fix.py`:

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.models.schemas import EvaluateResponse, Dimension, FixResponse
from backend.main import app

client = TestClient(app)

SAMPLE_EVAL = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=5, issues=["vague"], suggestions=["be specific"]),
    Dimension(name="Role / Persona Definition", score=3, issues=["no role"], suggestions=["add role"]),
    Dimension(name="Output Format Instructions", score=4, issues=[], suggestions=[]),
    Dimension(name="Context & Background", score=6, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=7, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=5, issues=[], suggestions=[]),
])

FIX_PAYLOAD_SINGLE = {
    "prompt": "Summarize this.",
    "evaluation": SAMPLE_EVAL.model_dump(),
    "mode": "single",
}

FIX_PAYLOAD_VARIANTS = {
    "prompt": "Summarize this.",
    "evaluation": SAMPLE_EVAL.model_dump(),
    "mode": "variants",
}


def test_fix_single_returns_fixed_prompt():
    mock_result = FixResponse(fixed_prompt="You are an expert. Summarize in 3 bullet points.")
    with patch("backend.routes.fix.fix_prompt", return_value=mock_result):
        response = client.post("/fix", json=FIX_PAYLOAD_SINGLE)
    assert response.status_code == 200
    assert "fixed_prompt" in response.json()


def test_fix_variants_returns_three_variants():
    mock_result = FixResponse(variants=["v1", "v2", "v3"])
    with patch("backend.routes.fix.fix_prompt", return_value=mock_result):
        response = client.post("/fix", json=FIX_PAYLOAD_VARIANTS)
    assert response.status_code == 200
    assert len(response.json()["variants"]) == 3


def test_fix_invalid_mode_returns_422():
    payload = {**FIX_PAYLOAD_SINGLE, "mode": "unknown"}
    response = client.post("/fix", json=payload)
    assert response.status_code == 422


def test_fix_llm_error_returns_503():
    with patch("backend.routes.fix.fix_prompt", side_effect=Exception("LLM down")):
        response = client.post("/fix", json=FIX_PAYLOAD_SINGLE)
    assert response.status_code == 503
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
pytest tests/test_routes_evaluate.py tests/test_routes_fix.py -v
```

Expected: Tests fail — routes are stubs.

- [ ] **Step 4: Implement `backend/routes/evaluate.py`**

```python
from fastapi import APIRouter, HTTPException
from backend.models.schemas import EvaluatRequest, EvaluateResponse
from backend.services.evaluator import evaluate_prompt

router = APIRouter()


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluatRequest):
    try:
        return evaluate_prompt(request.prompt)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

- [ ] **Step 5: Implement `backend/routes/fix.py`**

```python
from fastapi import APIRouter, HTTPException
from backend.models.schemas import FixRequest, FixResponse
from backend.services.fixer import fix_prompt

router = APIRouter()


@router.post("/fix", response_model=FixResponse)
def fix(request: FixRequest):
    try:
        return fix_prompt(request.prompt, request.evaluation, request.mode)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
pytest tests/test_routes_evaluate.py tests/test_routes_fix.py -v
```

Expected: All 8 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add backend/routes/evaluate.py backend/routes/fix.py tests/test_routes_evaluate.py tests/test_routes_fix.py
git commit -m "feat: add /evaluate and /fix FastAPI routes"
```

---

## Task 9: FastAPI Route — Export

**Files:**
- Modify: `backend/routes/export.py`
- Test: `tests/test_routes_export.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_routes_export.py`:

```python
import json
import pytest
from fastapi.testclient import TestClient
from backend.models.schemas import EvaluateResponse, Dimension
from backend.main import app

client = TestClient(app)

SAMPLE_EVAL = EvaluateResponse(dimensions=[
    Dimension(name="Clarity & Specificity", score=7, issues=[], suggestions=[]),
    Dimension(name="Role / Persona Definition", score=5, issues=[], suggestions=[]),
    Dimension(name="Output Format Instructions", score=6, issues=[], suggestions=[]),
    Dimension(name="Context & Background", score=8, issues=[], suggestions=[]),
    Dimension(name="Constraints & Guardrails", score=9, issues=[], suggestions=[]),
    Dimension(name="Tone & Style", score=7, issues=[], suggestions=[]),
])


def test_export_returns_json_file():
    payload = {
        "original_prompt": "Write a summary",
        "evaluation": SAMPLE_EVAL.model_dump(),
        "fixed_prompt": "You are an expert. Write a concise summary.",
        "mode": "single",
    }
    response = client.post("/export", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = json.loads(response.content)
    assert data["original_prompt"] == "Write a summary"
    assert "timestamp" in data
    assert data["mode"] == "single"


def test_export_includes_variants_when_provided():
    payload = {
        "original_prompt": "Write a summary",
        "evaluation": SAMPLE_EVAL.model_dump(),
        "variants": ["v1", "v2", "v3"],
        "mode": "variants",
    }
    response = client.post("/export", json=payload)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["variants"] == ["v1", "v2", "v3"]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_routes_export.py -v
```

Expected: Tests fail — export route is a stub.

- [ ] **Step 3: Implement `backend/routes/export.py`**

```python
from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.models.schemas import ExportRequest

router = APIRouter()


@router.post("/export")
def export(request: ExportRequest):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "original_prompt": request.original_prompt,
        "evaluation": request.evaluation.model_dump(),
        "fixed_prompt": request.fixed_prompt,
        "variants": request.variants,
        "mode": request.mode,
    }
    return JSONResponse(
        content=payload,
        headers={"Content-Disposition": 'attachment; filename="pef_export.json"'},
    )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_routes_export.py -v
```

Expected: All 2 tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
pytest tests/ -v
```

Expected: All tests PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/routes/export.py tests/test_routes_export.py
git commit -m "feat: add /export route returning downloadable JSON"
```

---

## Task 10: Streamlit Entry Point

**Files:**
- Create: `frontend/app.py`

- [ ] **Step 1: Implement `frontend/app.py`**

```python
import streamlit as st

st.set_page_config(
    page_title="Prompt Evaluation Framework",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Prompt Evaluation Framework")
st.markdown("""
Welcome to the **Prompt Evaluation Framework (PEF)** — an AI-powered tool to analyze and improve your LLM prompts.

Use the sidebar to navigate:
- **Get Started** — learn how to use the tool
- **Evaluate & Fix** — analyze and improve your prompts
- **Settings** — configure your Databricks connection
""")
```

- [ ] **Step 2: Verify Streamlit entry point starts without errors**

```bash
streamlit run frontend/app.py --server.headless true &
sleep 3
curl -s http://localhost:8501 | grep -q "Prompt Evaluation" && echo "OK" || echo "FAIL"
kill %1
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add frontend/app.py
git commit -m "feat: add Streamlit entry point"
```

---

## Task 11: Streamlit — Get Started Page

**Files:**
- Create: `frontend/pages/1_Get_Started.py`

- [ ] **Step 1: Implement `frontend/pages/1_Get_Started.py`**

```python
import streamlit as st

st.set_page_config(page_title="Get Started — PEF", page_icon="📖", layout="wide")

st.title("Get Started")
st.markdown("---")

st.header("What is PEF?")
st.markdown("""
The **Prompt Evaluation Framework** analyzes any LLM prompt and tells you exactly what's working, what isn't, and how to fix it — powered by AI.
""")

st.header("How It Works")
st.markdown("""
1. **Paste your prompt** on the *Evaluate & Fix* page
2. **Click Evaluate** — the AI scores your prompt across 6 quality dimensions
3. **Review the scorecard** — see exactly which issues were found and how to fix them
4. **Click Fix Prompt** — get an improved version of your prompt instantly
5. **Export** your results as JSON for your records
""")

st.header("Evaluation Dimensions")
dimensions = [
    ("Clarity & Specificity", "Is the prompt unambiguous and precise?"),
    ("Role / Persona Definition", "Is there a clear role or persona set for the model?"),
    ("Output Format Instructions", "Does the prompt specify the desired output format?"),
    ("Context & Background", "Is sufficient context provided for the task?"),
    ("Constraints & Guardrails", "Are limitations and boundaries clearly stated?"),
    ("Tone & Style", "Is the desired tone and style specified?"),
]
for name, desc in dimensions:
    st.markdown(f"**{name}** — {desc}")

st.header("Example Prompts to Try")

with st.expander("Bad prompt (before)"):
    st.code("Write something about climate change.", language=None)

with st.expander("Good prompt (after)"):
    st.code(
        "You are an environmental science communicator writing for a general audience. "
        "Write a 200-word explanation of the greenhouse effect and its relationship to "
        "climate change. Use simple language, avoid jargon, and end with one actionable "
        "step readers can take. Format as plain paragraphs.",
        language=None,
    )

st.header("Setup & Configuration")
st.markdown("""
Before using the tool, make sure your Databricks credentials are configured:
1. Go to the **Settings** page
2. Enter your **Databricks Base URL**, **LLM Endpoint URL**, and **API Token**
3. Click **Save Settings**

You only need to do this once — settings are persisted on the server.
""")
```

- [ ] **Step 2: Commit**

```bash
git add frontend/pages/1_Get_Started.py
git commit -m "feat: add Get Started documentation page"
```

---

## Task 12: Streamlit — Settings Page

**Files:**
- Create: `frontend/pages/3_Settings.py`

- [ ] **Step 1: Implement `frontend/pages/3_Settings.py`**

```python
import os
import httpx
import streamlit as st

st.set_page_config(page_title="Settings — PEF", page_icon="⚙️", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def load_current_config() -> dict:
    try:
        resp = httpx.get(f"{BACKEND_URL}/config", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}


def save_config(base_url: str, llm_url: str, token: str) -> bool:
    try:
        resp = httpx.post(
            f"{BACKEND_URL}/config",
            json={
                "databricks_base_url": base_url,
                "llm_endpoint_url": llm_url,
                "api_token": token,
            },
            timeout=5,
        )
        resp.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Failed to save settings: {e}")
        return False


st.title("Settings")
st.markdown("Configure your Databricks connection. Settings are saved to the server and persist across sessions.")
st.markdown("---")

current = load_current_config()

with st.form("settings_form"):
    base_url = st.text_input(
        "Databricks Base URL",
        value=current.get("databricks_base_url", ""),
        placeholder="https://<workspace>.azuredatabricks.net",
    )
    llm_url = st.text_input(
        "LLM Endpoint URL",
        value=current.get("llm_endpoint_url", ""),
        placeholder="https://<workspace>.azuredatabricks.net/serving-endpoints/<model>/invocations",
    )
    token = st.text_input(
        "API Token (PAT)",
        type="password",
        value="",
        placeholder="Enter new token to update, leave blank to keep existing",
    )

    token_status = current.get("api_token_set", False)
    if token_status:
        st.caption("✅ A token is currently saved on the server.")
    else:
        st.caption("⚠️ No token configured yet.")

    submitted = st.form_submit_button("Save Settings", type="primary")

if submitted:
    if not base_url or not llm_url:
        st.error("Databricks Base URL and LLM Endpoint URL are required.")
    else:
        final_token = token if token else (current.get("api_token", "") or "")
        if not final_token:
            st.error("API Token is required. No existing token found on server.")
        elif save_config(base_url, llm_url, final_token):
            st.success("✅ Settings saved successfully.")
```

- [ ] **Step 2: Commit**

```bash
git add frontend/pages/3_Settings.py
git commit -m "feat: add Settings page for Databricks config management"
```

---

## Task 13: Streamlit — Evaluate & Fix Page

**Files:**
- Create: `frontend/pages/2_Evaluate_Fix.py`

- [ ] **Step 1: Implement `frontend/pages/2_Evaluate_Fix.py`**

```python
import os
import json
import httpx
import streamlit as st
from datetime import datetime, timezone

st.set_page_config(page_title="Evaluate & Fix — PEF", page_icon="🔍", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def call_evaluate(prompt: str) -> dict:
    resp = httpx.post(f"{BACKEND_URL}/evaluate", json={"prompt": prompt}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def call_fix(prompt: str, evaluation: dict, mode: str) -> dict:
    resp = httpx.post(
        f"{BACKEND_URL}/fix",
        json={"prompt": prompt, "evaluation": evaluation, "mode": mode},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def call_export(original: str, evaluation: dict, fixed_prompt: str | None, variants: list | None, mode: str) -> bytes:
    resp = httpx.post(
        f"{BACKEND_URL}/export",
        json={
            "original_prompt": original,
            "evaluation": evaluation,
            "fixed_prompt": fixed_prompt,
            "variants": variants,
            "mode": mode,
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.content


def render_scorecard(evaluation: dict):
    dimensions = evaluation.get("dimensions", [])
    if not dimensions:
        return

    st.subheader("Evaluation Scorecard")
    for dim in dimensions:
        score = dim["score"]
        color = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
        with st.expander(f"{color} {dim['name']} — {score}/10"):
            if dim["issues"]:
                st.markdown("**Issues:**")
                for issue in dim["issues"]:
                    st.markdown(f"- {issue}")
            else:
                st.markdown("**Issues:** None found ✅")

            if dim["suggestions"]:
                st.markdown("**Suggestions:**")
                for s in dim["suggestions"]:
                    st.markdown(f"- {s}")


st.title("Evaluate & Fix")
st.markdown("Paste any LLM prompt below to get a scored evaluation and AI-powered improvements.")
st.markdown("---")

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None
if "original_prompt" not in st.session_state:
    st.session_state.original_prompt = ""
if "fix_result" not in st.session_state:
    st.session_state.fix_result = None
if "fix_mode" not in st.session_state:
    st.session_state.fix_mode = "single"

prompt = st.text_area(
    "Your Prompt",
    height=200,
    placeholder="Paste your LLM prompt here...",
    value=st.session_state.original_prompt,
)

col1, col2 = st.columns([1, 3])
with col1:
    evaluate_clicked = st.button("Evaluate", type="primary", use_container_width=True)

if evaluate_clicked:
    if not prompt.strip():
        st.error("Please enter a prompt to evaluate.")
    else:
        with st.spinner("Analyzing your prompt..."):
            try:
                result = call_evaluate(prompt.strip())
                st.session_state.evaluation = result
                st.session_state.original_prompt = prompt.strip()
                st.session_state.fix_result = None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 503:
                    st.error("Could not reach the LLM. Please check your Settings.")
                else:
                    st.error(f"Error: {e.response.text}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

if st.session_state.evaluation:
    render_scorecard(st.session_state.evaluation)

    st.markdown("---")
    st.subheader("Fix Your Prompt")

    fix_mode = st.radio(
        "Fix mode:",
        options=["single", "variants"],
        format_func=lambda x: "Single best fix" if x == "single" else "3 variants to compare",
        horizontal=True,
    )
    st.session_state.fix_mode = fix_mode

    fix_clicked = st.button("Fix Prompt", type="primary")

    if fix_clicked:
        with st.spinner("Generating improved prompt..."):
            try:
                result = call_fix(
                    st.session_state.original_prompt,
                    st.session_state.evaluation,
                    fix_mode,
                )
                st.session_state.fix_result = result
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 503:
                    st.error("Could not reach the LLM. Please check your Settings.")
                else:
                    st.error(f"Error: {e.response.text}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    if st.session_state.fix_result:
        fix_result = st.session_state.fix_result
        st.markdown("---")
        st.subheader("Improved Prompt")

        if fix_result.get("fixed_prompt"):
            fixed = st.text_area(
                "Fixed Prompt (editable)",
                value=fix_result["fixed_prompt"],
                height=200,
            )
            export_fixed = fixed
            export_variants = None
        else:
            variants = fix_result.get("variants", [])
            tabs = st.tabs([f"Variant {i+1}" for i in range(len(variants))])
            for i, (tab, v) in enumerate(zip(tabs, variants)):
                with tab:
                    st.text_area(f"Variant {i+1} (editable)", value=v, height=200, key=f"variant_{i}")
            export_fixed = None
            export_variants = variants

        try:
            export_bytes = call_export(
                st.session_state.original_prompt,
                st.session_state.evaluation,
                export_fixed,
                export_variants,
                st.session_state.fix_mode,
            )
            st.download_button(
                label="Export as JSON",
                data=export_bytes,
                file_name=f"pef_export_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )
        except Exception:
            st.warning("Export unavailable. Backend may be unreachable.")
```

- [ ] **Step 2: Commit**

```bash
git add frontend/pages/2_Evaluate_Fix.py
git commit -m "feat: add Evaluate & Fix main page with scorecard, fix modes, and export"
```

---

## Task 14: Full Integration Smoke Test

- [ ] **Step 1: Start backend**

```bash
uvicorn backend.main:app --port 8000 &
sleep 2
```

- [ ] **Step 2: Verify backend is running**

```bash
curl -s http://localhost:8000/docs | grep -q "PEF API" && echo "Backend OK" || echo "Backend FAIL"
```

Expected: `Backend OK`

- [ ] **Step 3: Run full test suite**

```bash
pytest tests/ -v
```

Expected: All tests PASS, 0 failures.

- [ ] **Step 4: Start frontend**

```bash
streamlit run frontend/app.py --server.port 8501 &
sleep 3
curl -s http://localhost:8501 | grep -q "Streamlit" && echo "Frontend OK" || echo "Frontend FAIL"
```

Expected: `Frontend OK`

- [ ] **Step 5: Kill background processes**

```bash
kill %1 %2 2>/dev/null || true
```

- [ ] **Step 6: Final commit**

```bash
git add .
git commit -m "feat: complete PEF implementation — Streamlit + FastAPI + Databricks LLM"
```

---

## Self-Review Checklist

- [x] **Settings page** — GET/POST /config routes, reads `config.json`, falls back to `.env` ✅
- [x] **Get Started page** — usage guide, dimension descriptions, example prompts ✅
- [x] **Evaluate & Fix page** — text area, evaluate button, scorecard, fix modes, export ✅
- [x] **Evaluate endpoint** — 6 dimensions, score + issues + suggestions, retry on bad JSON ✅
- [x] **Fix endpoint** — single mode returns `fixed_prompt`, variants mode returns 3 items ✅
- [x] **Export endpoint** — returns JSON file with timestamp, original, evaluation, fixed ✅
- [x] **config.json takes precedence over .env** — implemented in ConfigManager ✅
- [x] **Token masked in GET /config response** — `api_token_set: bool` only ✅
- [x] **503 on LLM errors** — all routes catch exceptions and return 503 ✅
- [x] **README.md and CLAUDE.md** — included in Task 1 scaffold ✅
- [x] **All test files have real code** — no "TBD" or placeholder tests ✅
