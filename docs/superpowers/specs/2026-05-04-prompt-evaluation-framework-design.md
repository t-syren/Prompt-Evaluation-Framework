# Prompt Evaluation Framework (PEF) — Design Spec

**Date:** 2026-05-04  
**Project:** Syren PEF  
**Status:** Approved

---

## Overview

A generic, AI-powered prompt evaluation and improvement platform. Users paste any LLM prompt, receive a structured scored evaluation across standard dimensions, and can trigger an AI-powered fix. Built by Syren for a client, designed to be generic enough to handle any prompt type or use case.

---

## Architecture

```
┌─────────────────────┐        HTTP        ┌──────────────────────┐
│   Streamlit UI      │ ──────────────────▶ │   FastAPI Backend    │
│                     │                     │                      │
│  - Prompt input     │ ◀────────────────── │  - /evaluate         │
│  - Eval report      │      JSON           │  - /fix              │
│  - Fix button       │                     │  - /export           │
│  - Export button    │                     │  - Databricks client │
└─────────────────────┘                     └──────────┬───────────┘
                                                       │ HTTPS + PAT
                                                       ▼
                                          ┌────────────────────────┐
                                          │  Databricks Claude LLM │
                                          │  (claude-sonnet-4-6)   │
                                          └────────────────────────┘
```

- **Streamlit** — pure UI layer, calls FastAPI via `httpx`
- **FastAPI** — all LLM logic, prompt engineering, response parsing
- **Databricks endpoint** — OpenAI-compatible API, authenticated with PAT token
- **Config** — runtime config stored in `config.json`, fallback to `.env`

---

## Pages

### 1. Get Started
- Overview of the tool and its purpose
- Step-by-step usage guide (how to evaluate, fix, and export)
- Example prompts to try
- Links to Databricks setup documentation

### 2. Evaluate & Fix (Main Tool)
Core user flow:
1. Paste prompt into text area
2. Click **"Evaluate"** → calls `POST /evaluate` → renders scored report
3. Scorecard shows each dimension: score (1–10), issues found, improvement suggestions
4. Toggle: **Single Fix** / **Multiple Variants** (default: Single Fix)
5. Click **"Fix Prompt"** → calls `POST /fix` → shows improved prompt(s) in editable text area
6. User can manually edit the fixed prompt
7. Click **"Export"** → downloads full session as `.json`

### 3. Settings
- Fields: Databricks Base URL, LLM Endpoint URL, API Token (masked)
- **"Save"** button writes to `config.json` on the server
- FastAPI reads `config.json` at request time — changes take effect immediately, no restart required
- If `config.json` is absent, FastAPI falls back to `.env`

---

## Evaluation Dimensions

Standard dimensions the AI evaluates against (AI may also flag issues outside these):

| # | Dimension | Description |
|---|-----------|-------------|
| 1 | Clarity & Specificity | Is the prompt unambiguous and precise? |
| 2 | Role / Persona Definition | Is there a clear role or persona set for the LLM? |
| 3 | Output Format Instructions | Does the prompt specify the desired output format? |
| 4 | Context & Background | Is sufficient context provided for the task? |
| 5 | Constraints & Guardrails | Are limitations and boundaries clearly stated? |
| 6 | Tone & Style | Is the desired tone/style specified? |

---

## API Endpoints

### `POST /evaluate`
**Request:**
```json
{ "prompt": "<user prompt text>" }
```
**Response:**
```json
{
  "dimensions": [
    {
      "name": "Clarity & Specificity",
      "score": 7,
      "issues": ["Vague objective in line 2"],
      "suggestions": ["Specify the exact output you expect"]
    }
  ]
}
```

### `POST /fix`
**Request:**
```json
{
  "prompt": "<original prompt>",
  "evaluation": { ... },
  "mode": "single" | "variants"
}
```
**Response (single):**
```json
{ "fixed_prompt": "<improved prompt>" }
```
**Response (variants):**
```json
{ "variants": ["<variant 1>", "<variant 2>", "<variant 3>"] }
```
*Always exactly 3 variants when mode is `variants`.*
```
```

### `POST /export`
**Request:**
```json
{
  "original_prompt": "...",
  "evaluation": { ... },
  "fixed_prompt": "..."
}
```
**Response:** Downloadable `.json` file

### `GET /config` / `POST /config`
- GET: returns current config (token masked)
- POST: updates `config.json`

---

## Project Structure

```
PEF/
├── frontend/
│   ├── app.py                    # Streamlit entry point + nav
│   └── pages/
│       ├── 1_Get_Started.py
│       ├── 2_Evaluate_Fix.py
│       └── 3_Settings.py
├── backend/
│   ├── main.py                   # FastAPI app init
│   ├── routes/
│   │   ├── evaluate.py
│   │   ├── fix.py
│   │   ├── export.py
│   │   └── config.py
│   ├── services/
│   │   ├── databricks_client.py  # Databricks API calls
│   │   ├── evaluator.py          # Evaluation prompt logic
│   │   └── fixer.py              # Fix prompt logic
│   └── models/
│       └── schemas.py            # Pydantic request/response models
├── config.json                   # Runtime config (gitignored)
├── .env                          # Fallback config (gitignored)
├── .gitignore
├── requirements.txt
├── README.md
└── CLAUDE.md
```

---

## Configuration

`config.json` schema:
```json
{
  "databricks_base_url": "https://...",
  "llm_endpoint_url": "https://.../invocations",
  "api_token": "dapi..."
}
```

Both `config.json` and `.env` are gitignored. `config.json` takes precedence over `.env`.

---

## LLM Integration

- Databricks endpoint is OpenAI-compatible — use `openai` Python SDK pointed at the Databricks URL
- Authentication: `Authorization: Bearer <PAT>` header
- Model: `databricks-claude-sonnet-4-6`
- Evaluation and fix logic are implemented as structured prompts in `services/evaluator.py` and `services/fixer.py`
- Responses are parsed into Pydantic models

---

## Error Handling

- If Databricks endpoint is unreachable: return 503 with a user-friendly message in the UI
- If config is missing: prompt user to go to Settings page
- If LLM returns malformed JSON: retry once, then return a generic error
- All errors surfaced in Streamlit as `st.error()` banners — no silent failures

---

## Export Format

```json
{
  "timestamp": "2026-05-04T10:30:00Z",
  "original_prompt": "...",
  "evaluation": {
    "dimensions": [ ... ]
  },
  "fixed_prompt": "...",
  "mode": "single"
}
```

---

## Deployment

- Deployed to **Databricks Apps**
- Frontend and backend run as separate services
- `config.json` persists on the Databricks Apps filesystem
- No external database required

---

## Out of Scope (MVP)

- User authentication / login
- Prompt version history / database storage
- Comparison between two prompts side-by-side
- Custom evaluation rubric builder (post-MVP)
