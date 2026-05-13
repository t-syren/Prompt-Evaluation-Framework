import os
import time
import threading
from typing import Optional, List, Tuple
import httpx
import streamlit as st
from datetime import datetime, timezone
from frontend.styles import base_css, nav_html, nav_close

st.set_page_config(page_title="Evaluate & Fix — PEF", page_icon=None, layout="wide",
                   initial_sidebar_state="collapsed")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.markdown(base_css(), unsafe_allow_html=True)
st.markdown(nav_html("evaluate"), unsafe_allow_html=True)

# Page-specific styles
st.markdown("""
<style>
.page-header { margin-bottom: 24px; animation: fadeUp 0.5s 0.05s both; }
.page-title  { font-size: 24px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.025em; margin-bottom: 6px; }
.page-sub    { font-size: 14px; color: rgba(255,255,255,0.35); line-height: 1.5; }

/* Prompt input card */
.prompt-card-header {
  padding: 14px 20px; border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center; gap: 8px;
}

/* Score overview */
.overall-score-row {
  padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center; gap: 20px;
}
.overall-num {
  font-size: 48px; font-weight: 800; font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, #FF3621, #ff8a75);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1;
}
.overall-denom { font-size: 20px; font-weight: 500; color: rgba(255,255,255,0.2); align-self: flex-end; margin-bottom: 6px; }
.overall-label { font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.5); }
.overall-sub   { font-size: 12px; color: rgba(255,255,255,0.25); margin-top: 2px; }

.score-grid {
  display: grid; grid-template-columns: repeat(4,1fr);
  gap: 1px; background: rgba(255,255,255,0.05);
}
.score-cell {
  background: rgba(9,9,14,0.6); padding: 16px 14px;
  display: flex; flex-direction: column; gap: 8px;
  cursor: pointer; transition: background 0.15s;
}
.score-cell:hover { background: rgba(255,255,255,0.03); }
.score-cell-top { display: flex; align-items: baseline; justify-content: space-between; }
.score-num-lg { font-size: 28px; font-weight: 800; font-family: 'JetBrains Mono', monospace; line-height: 1; }
.score-denom  { font-size: 11px; color: rgba(255,255,255,0.25); }
.score-dim-label { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.35); letter-spacing: 0.04em; }
.score-bar-track { height: 2px; background: rgba(255,255,255,0.08); border-radius: 1px; overflow: hidden; }
.score-bar-fill  { height: 100%; border-radius: 1px; transition: width 1s cubic-bezier(0.25,0.46,0.45,0.94); }

.sg { color: #4ade80 !important; }
.sw { color: #fbbf24 !important; }
.sb { color: #f87171 !important; }
.bg { background: linear-gradient(90deg,#16a34a,#4ade80) !important; }
.bw { background: linear-gradient(90deg,#d97706,#fbbf24) !important; }
.bb { background: linear-gradient(90deg,#dc2626,#f87171) !important; }

/* Dimension detail rows */
.detail-row {
  padding: 16px 20px; border-bottom: 1px solid rgba(255,255,255,0.05);
  display: grid; grid-template-columns: 180px 1fr 1fr; gap: 16px; align-items: start;
}
.detail-row:last-child { border-bottom: none; }
.detail-dim { display: flex; align-items: center; gap: 10px; }
.detail-badge {
  width: 36px; height: 36px; border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; font-weight: 800; font-family: 'JetBrains Mono', monospace; flex-shrink: 0;
}
.badge-g { background: rgba(22,163,74,0.15); color: #4ade80; }
.badge-w { background: rgba(217,119,6,0.15);  color: #fbbf24; }
.badge-b { background: rgba(220,38,38,0.15);  color: #f87171; }
.detail-dim-name { font-size: 12.5px; font-weight: 600; color: rgba(255,255,255,0.7); line-height: 1.3; }
.detail-col-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
  color: rgba(255,255,255,0.25); margin-bottom: 6px;
}
.detail-item { font-size: 12px; color: rgba(255,255,255,0.45); line-height: 1.5; display: flex; align-items: flex-start; gap: 6px; margin-bottom: 4px; }
.detail-dot  { width: 4px; height: 4px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }

/* Action cards */
.action-row { display: flex; gap: 12px; margin-bottom: 20px; }
.action-card {
  flex: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px; padding: 18px 20px; cursor: pointer;
  transition: background 0.2s, border-color 0.2s, transform 0.2s;
}
.action-card:hover { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); transform: translateY(-2px); }
.action-card.primary-action { border-color: rgba(255,54,33,0.3); background: rgba(255,54,33,0.07); }
.action-card.primary-action:hover { background: rgba(255,54,33,0.12); border-color: rgba(255,54,33,0.45); }
.action-icon {
  width: 36px; height: 36px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; margin-bottom: 12px;
}
.ai-red   { background: rgba(255,54,33,0.2); }
.ai-indigo{ background: rgba(99,102,241,0.2); }
.ai-teal  { background: rgba(20,184,166,0.15); }
.action-title { font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; letter-spacing: -0.01em; }
.action-desc  { font-size: 12px; color: rgba(255,255,255,0.35); line-height: 1.5; }

/* Result tiles */
.result-tile {
  margin-top: 16px; background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 16px 20px;
}
.result-tile-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.result-tile-title  { font-size: 15px; font-weight: 700; color: #f1f5f9; }
.score-badge-pill {
  font-weight: 700; font-size: 13px; padding: 3px 10px; border-radius: 20px;
}

/* Comparison table */
.compare-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.compare-title { font-size: 16px; font-weight: 700; color: #f1f5f9; }
.compare-table {
  background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px; padding: 6px 16px 2px;
}
.compare-col-headers {
  display: grid; grid-template-columns: 2fr 1fr 1fr 0.7fr; gap: 8px;
  padding-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.08);
}
.compare-col-hdr { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.25); text-transform: uppercase; letter-spacing: 0.05em; text-align: center; }
.compare-col-hdr:first-child { text-align: left; }
.compare-row {
  display: grid; grid-template-columns: 2fr 1fr 1fr 0.7fr; gap: 8px;
  align-items: center; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
}
.compare-row:last-child { border-bottom: none; }
.compare-dim  { font-size: 13px; color: rgba(255,255,255,0.6); font-weight: 500; }
.score-mini   {
  border-radius: 6px; text-align: center; padding: 3px 6px;
}
.delta-cell   { text-align: center; font-size: 13px; font-weight: 700; }

/* Fix section */
.fix-section-title { font-size: 18px; font-weight: 700; color: #f1f5f9; margin-bottom: 14px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <div class="page-title">Evaluate &amp; Fix</div>
  <div class="page-sub">Score any LLM prompt across 8 quality dimensions · Auto-fix · Stress test · Hallucination check</div>
</div>
""", unsafe_allow_html=True)


# ── API helpers ───────────────────────────────────────────────────────────────
def call_evaluate_dimensions(prompt: str) -> dict:
    resp = httpx.post(f"{BACKEND_URL}/evaluate/dimensions", json={"prompt": prompt}, timeout=360)
    resp.raise_for_status()
    return resp.json()


def call_evaluate_safety(prompt: str) -> dict:
    resp = httpx.post(f"{BACKEND_URL}/evaluate/safety", json={"prompt": prompt}, timeout=120)
    resp.raise_for_status()
    return resp.json()


def call_evaluate(prompt: str) -> dict:
    """Full evaluation combining dimensions + safety. Used for validate improvement."""
    resp = httpx.post(f"{BACKEND_URL}/evaluate", json={"prompt": prompt}, timeout=480)
    resp.raise_for_status()
    return resp.json()


def call_fix(prompt: str, evaluation: dict, mode: str) -> dict:
    resp = httpx.post(
        f"{BACKEND_URL}/fix/generate",
        json={"prompt": prompt, "evaluation": evaluation, "mode": mode},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def call_fix_validate(original_prompt: str, fixed_prompt: str, original_evaluation: dict) -> dict:
    resp = httpx.post(
        f"{BACKEND_URL}/fix/validate",
        json={
            "original_prompt": original_prompt,
            "fixed_prompt": fixed_prompt,
            "original_evaluation": original_evaluation,
        },
        timeout=480,
    )
    resp.raise_for_status()
    return resp.json()


def call_refine(original: str, current_fixed: str, evaluation: dict, feedback: str, mode: str) -> dict:
    resp = httpx.post(
        f"{BACKEND_URL}/refine",
        json={
            "original_prompt": original,
            "current_fixed": current_fixed,
            "evaluation": evaluation,
            "feedback": feedback,
            "mode": mode,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def call_stress_test(prompt: str, num_attacks: int) -> dict:
    resp = httpx.post(
        f"{BACKEND_URL}/stress-test",
        json={"prompt": prompt, "num_attacks": num_attacks},
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()


def call_hallucination_check(prompt: str) -> dict:
    resp = httpx.post(
        f"{BACKEND_URL}/hallucination-check",
        json={"prompt": prompt},
        timeout=240,
    )
    resp.raise_for_status()
    return resp.json()


# ── Background pipeline ───────────────────────────────────────────────────────
def _run_pipeline_bg(
    prompt: str, bg: dict, cancel_ev: threading.Event,
    auto_stress: bool, auto_hallucination: bool,
    auto_fix: bool, auto_eval_improvement: bool, attack_count: int,
) -> None:
    """Runs evaluation pipeline in a background thread. Writes into bg dict."""
    try:
        bg["progress"].append("⏳ Running 6 quality dimensions via G-Eval in parallel…")
        if cancel_ev.is_set():
            bg["cancelled"] = True
            return
        dims = call_evaluate_dimensions(prompt)
        for d in dims["dimensions"]:
            bg["progress"].append(f"✅ {d['name']} — {d['score']}/10")

        if cancel_ev.is_set():
            bg["cancelled"] = True
            return

        bg["progress"].append("⏳ Checking Bias & Toxicity safety metrics…")
        safety = call_evaluate_safety(prompt)
        for d in safety["dimensions"]:
            bg["progress"].append(f"✅ {d['name']} — {d['score']}/10")

        combined = {"dimensions": dims["dimensions"] + safety["dimensions"]}
        bg["evaluation"] = combined

        if cancel_ev.is_set():
            bg["cancelled"] = True
            return

        if auto_stress:
            bg["progress"].append(f"⏳ Running stress test ({attack_count} attacks)…")
            sr = call_stress_test(prompt, attack_count)
            bg["stress_result"] = sr
            bg["progress"].append(f"✅ Stress test — robustness {sr['vulnerability_score']}/10")
            if cancel_ev.is_set():
                bg["cancelled"] = True
                return

        if auto_hallucination:
            bg["progress"].append("⏳ Checking hallucination risk…")
            hr = call_hallucination_check(prompt)
            bg["hallucination_result"] = hr
            bg["progress"].append(f"✅ Hallucination — {hr['verdict']} ({hr['hallucination_score']}/10)")
            if cancel_ev.is_set():
                bg["cancelled"] = True
                return

        if auto_fix:
            bg["progress"].append("⏳ Generating improved prompt…")
            fr = call_fix(prompt, combined, "single")
            bg["fix_result"] = fr
            bg["progress"].append("✅ Improved prompt generated")

            if auto_eval_improvement and fr.get("fixed_prompt"):
                if cancel_ev.is_set():
                    bg["cancelled"] = True
                    return
                bg["progress"].append("⏳ Validating improvement (regression + safety)…")
                vr = call_fix_validate(prompt, fr["fixed_prompt"], combined)
                bg["fix_validate_result"] = vr
                bg["progress"].append("✅ Improvement validated")

        bg["done"] = True
    except Exception as e:
        bg["error"] = str(e)


# ── UI helpers ────────────────────────────────────────────────────────────────
def score_color(score: int) -> Tuple[str, str, str]:
    """Returns (text_color, bg_color, border_color) based on score."""
    if score >= 7:
        return "#16a34a", "#f0fdf4", "#bbf7d0"
    if score >= 4:
        return "#d97706", "#fffbeb", "#fde68a"
    return "#dc2626", "#fef2f2", "#fecaca"


def score_emoji(score: int) -> str:
    if score >= 7:
        return "🟢"
    if score >= 4:
        return "🟡"
    return "🔴"


def render_score_overview(dimensions: list):
    """8-cell grid: large mono score + colour bar per dimension."""
    def _classes(score: int):
        if score >= 7: return "sg", "bg"
        if score >= 4: return "sw", "bw"
        return "sb", "bb"

    cells = ""
    for dim in dimensions:
        s = dim["score"]
        nc, bc = _classes(s)
        short = dim["name"].split(" & ")[0].split(" / ")[0]
        pct = s * 10
        cells += f"""
<div class="score-cell">
  <div class="score-cell-top">
    <span class="score-num-lg {nc}">{s}</span>
    <span class="score-denom">/10</span>
  </div>
  <div class="score-dim-label">{short.upper()}</div>
  <div class="score-bar-track"><div class="score-bar-fill {bc}" style="width:{pct}%"></div></div>
</div>"""

    avg = sum(d["score"] for d in dimensions) / len(dimensions) if dimensions else 0
    issues = sum(1 for d in dimensions if d["score"] < 7)
    issue_txt = f"{issues} need{'s' if issues == 1 else ''} attention" if issues else "all passing"

    st.markdown(f"""
<div class="glass-card" style="animation:fadeUp 0.5s 0.1s both;">
  <div class="overall-score-row">
    <div>
      <div style="display:flex;align-items:baseline;gap:4px;">
        <span class="overall-num">{avg:.1f}</span>
        <span class="overall-denom">/10</span>
      </div>
      <div class="overall-label">Overall Score</div>
      <div class="overall-sub">8 dimensions evaluated · {issue_txt}</div>
    </div>
  </div>
  <div class="score-grid">{cells}</div>
</div>
""", unsafe_allow_html=True)


def render_scorecard_details(dimensions: list):
    """Detail rows with badge + issues/suggestions columns, then Streamlit expander for full reasoning."""
    st.markdown("<div class='glass-card' style='animation:fadeUp 0.5s 0.15s both;'>", unsafe_allow_html=True)
    st.markdown("""
<div class="glass-card-header">
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M2 4h10M2 7h6M2 10h8" stroke="rgba(255,255,255,0.35)" stroke-width="1.4" stroke-linecap="round"/>
  </svg>
  <span class="card-label">Dimension Analysis</span>
  <span style="margin-left:auto;font-size:11px;color:rgba(255,255,255,0.2);">Expand any row for full reasoning</span>
</div>""", unsafe_allow_html=True)

    for dim in dimensions:
        score = dim["score"]
        if score >= 7:
            badge_cls, dot_col = "badge-g", "#4ade80"
            row_bg = ""
        elif score >= 4:
            badge_cls, dot_col = "badge-w", "#fbbf24"
            row_bg = "background:rgba(217,119,6,0.04);"
        else:
            badge_cls, dot_col = "badge-b", "#f87171"
            row_bg = "background:rgba(220,38,38,0.04);"

        issues_html = "".join(
            f'<div class="detail-item"><div class="detail-dot" style="background:{dot_col}"></div>{i}</div>'
            for i in dim["issues"]
        ) or f'<div class="detail-item" style="color:rgba(74,222,128,0.5);">No critical issues</div>'

        suggs_html = "".join(
            f'<div class="detail-item"><div class="detail-dot" style="background:#4ade80"></div>{s}</div>'
            for s in dim["suggestions"]
        ) or '<div class="detail-item" style="color:rgba(255,255,255,0.25);">See reasoning below</div>'

        st.markdown(f"""
<div class="detail-row" style="{row_bg}">
  <div class="detail-dim">
    <div class="detail-badge {badge_cls}">{score}</div>
    <div class="detail-dim-name">{dim['name']}</div>
  </div>
  <div>
    <div class="detail-col-label">Issues</div>
    {issues_html}
  </div>
  <div>
    <div class="detail-col-label">Suggestions</div>
    {suggs_html}
  </div>
</div>""", unsafe_allow_html=True)

        if dim.get("reasoning"):
            with st.expander(f"Full reasoning — {dim['name']}"):
                st.progress(score / 10)
                st.markdown(dim["reasoning"])

    st.markdown("</div>", unsafe_allow_html=True)


def render_comparison(original_eval: dict, fixed_eval: dict):
    """Before/after score comparison table in Glass Premium style."""
    orig_dims = {d["name"]: d["score"] for d in original_eval.get("dimensions", [])}
    fix_dims  = {d["name"]: d["score"] for d in fixed_eval.get("dimensions", [])}
    orig_avg  = sum(orig_dims.values()) / len(orig_dims) if orig_dims else 0
    fix_avg   = sum(fix_dims.values())  / len(fix_dims)  if fix_dims  else 0
    total_d   = fix_avg - orig_avg

    td_color = "#4ade80" if total_d > 0 else ("#f87171" if total_d < 0 else "#64748b")
    td_bg    = "rgba(22,163,74,0.12)" if total_d > 0 else ("rgba(220,38,38,0.12)" if total_d < 0 else "rgba(100,116,139,0.12)")
    td_sign  = "+" if total_d > 0 else ""
    td_arrow = "↑" if total_d > 0 else ("↓" if total_d < 0 else "→")

    def _mini(score: int) -> str:
        tc, bg = ("#4ade80", "rgba(22,163,74,0.12)") if score >= 7 else \
                 (("#fbbf24", "rgba(217,119,6,0.12)") if score >= 4 else ("#f87171", "rgba(220,38,38,0.12)"))
        return (f'<div class="score-mini" style="background:{bg};border:1px solid {tc}22;">'
                f'<span style="font-size:15px;font-weight:800;font-family:JetBrains Mono,monospace;color:{tc};">{score}</span>'
                f'<span style="font-size:11px;color:rgba(255,255,255,0.25);">/10</span></div>')

    rows = ""
    for name in orig_dims:
        o = orig_dims.get(name, 0)
        f = fix_dims.get(name, o)
        d = f - o
        dc = "#4ade80" if d > 0 else ("#f87171" if d < 0 else "rgba(255,255,255,0.25)")
        ds = "+" if d > 0 else ""
        da = "↑" if d > 0 else ("↓" if d < 0 else "—")
        rows += f"""
<div class="compare-row">
  <span class="compare-dim">{name}</span>
  {_mini(o)}
  {_mini(f)}
  <div class="delta-cell" style="color:{dc};">{da} {ds}{d}</div>
</div>"""

    st.markdown(f"""
<div style="margin-top:20px;">
  <div class="compare-header">
    <span class="compare-title">Score Comparison</span>
    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
      <span style="font-size:13px;color:rgba(255,255,255,0.4);">Before: <strong style="color:#f1f5f9;">{orig_avg:.1f}/10</strong></span>
      <span style="color:rgba(255,255,255,0.2);font-size:16px;">→</span>
      <span style="font-size:13px;color:rgba(255,255,255,0.4);">After: <strong style="color:#f1f5f9;">{fix_avg:.1f}/10</strong></span>
      <span style="background:{td_bg};color:{td_color};font-weight:700;font-size:13px;padding:3px 12px;border-radius:20px;">
        {td_arrow} {td_sign}{total_d:.1f}
      </span>
    </div>
  </div>
  <div class="compare-table">
    <div class="compare-col-headers">
      <span class="compare-col-hdr" style="text-align:left;">Dimension</span>
      <span class="compare-col-hdr">Before</span>
      <span class="compare-col-hdr">After</span>
      <span class="compare-col-hdr">Delta</span>
    </div>
    {rows}
  </div>
</div>
""", unsafe_allow_html=True)


def build_scorecard_report(
    evaluation: dict,
    original_prompt: str,
    stress_result: Optional[dict] = None,
    hallucination_result: Optional[dict] = None,
) -> str:
    """Build a human-readable text report of the evaluation."""
    dims = evaluation.get("dimensions", [])
    avg = sum(d["score"] for d in dims) / len(dims) if dims else 0
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    bar_len = 20

    lines = [
        "PROMPT EVALUATION REPORT",
        "=" * 50,
        f"Generated: {ts}",
        f"Overall Score: {avg:.1f} / 10",
        "",
        "ORIGINAL PROMPT",
        "-" * 50,
        original_prompt,
        "",
        "DIMENSION SCORES",
        "-" * 50,
    ]
    for d in dims:
        filled = round(d["score"] / 10 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        lines.append(f"  {d['name']:<38} {d['score']:2}/10  [{bar}]")

    lines += ["", "DETAILED FINDINGS", "-" * 50]
    for d in dims:
        lines += ["", f"▌ {d['name']}  ({d['score']}/10)"]
        if d.get("reasoning"):
            lines.append(f"  Analysis: {d['reasoning']}")
        if d["issues"]:
            lines.append("  Issues:")
            for i in d["issues"]:
                lines.append(f"    • {i}")
        if d["suggestions"]:
            lines.append("  Suggestions:")
            for s in d["suggestions"]:
                lines.append(f"    • {s}")
        if not d["issues"] and not d["suggestions"]:
            lines.append("  No specific issues listed — see analysis above.")

    if stress_result:
        lines += ["", "", "STRESS TEST RESULTS", "-" * 50]
        lines.append(f"  Robustness Score: {stress_result['vulnerability_score']}/10")
        lines.append("")
        for attack in stress_result.get("attacks", []):
            verdict_label = "Broke intent" if attack["verdict"] == "PASS" else "Intent preserved"
            lines.append(f"  [{attack['attack_type']}] {verdict_label}")
            lines.append(f"    Input:  {attack['input']}")
            lines.append(f"    Reason: {attack['reason']}")

    if hallucination_result:
        lines += ["", "", "HALLUCINATION RISK", "-" * 50]
        lines.append(f"  Score:   {hallucination_result['hallucination_score']}/10")
        lines.append(f"  Verdict: {hallucination_result['verdict']}")
        lines.append(f"  Reason:  {hallucination_result['reason']}")
        lines.append("")
        lines.append("  Sample output used for analysis:")
        lines.append(f"  {hallucination_result['sample_output']}")

    return "\n".join(lines)


# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("evaluation", None), ("original_prompt", ""),
    ("fix_result", None), ("fix_mode", "single"),
    ("fix_evaluation", None), ("variant_evaluations", None),
    ("stress_test_result", None), ("hallucination_result", None),
    ("fix_validate_result", None),
    ("eval_running", False), ("eval_bg_state", None), ("eval_cancel_event", None),
    ("prompt_clear_counter", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Always reload config so Settings changes are reflected immediately
try:
    cfg_resp = httpx.get(f"{BACKEND_URL}/config", timeout=5)
    _cfg = cfg_resp.json() if cfg_resp.status_code == 200 else {}
except Exception:
    _cfg = {}

_auto_stress = _cfg.get("auto_stress_test", False)
_auto_hallucination = _cfg.get("auto_hallucination_check", False)
_auto_fix = _cfg.get("auto_fix_prompt", False)
_auto_eval_improvement = _cfg.get("auto_evaluate_improvement", False)
_attack_count = _cfg.get("stress_test_attack_count", 5)


# ── Running status (shown on every render while bg thread is active) ──────────
if st.session_state.eval_running:
    bg = st.session_state.eval_bg_state or {}

    if bg.get("done"):
        # Harvest results from bg dict into session state
        st.session_state.evaluation = bg["evaluation"]
        st.session_state.original_prompt = st.session_state.get("_pending_prompt", "")
        if bg.get("stress_result"):
            st.session_state.stress_test_result = bg["stress_result"]
        if bg.get("hallucination_result"):
            st.session_state.hallucination_result = bg["hallucination_result"]
        if bg.get("fix_result"):
            st.session_state.fix_result = bg["fix_result"]
        if bg.get("fix_validate_result"):
            vr = bg["fix_validate_result"]
            st.session_state.fix_evaluation = vr["post_eval"]
            st.session_state.fix_validate_result = vr
        st.session_state.eval_running = False
        st.session_state.eval_bg_state = None
        st.rerun()
    elif bg.get("error"):
        st.error(f"Analysis error: {bg['error']}")
        st.session_state.eval_running = False
    elif bg.get("cancelled"):
        st.info("Analysis cancelled.")
        st.session_state.eval_running = False
    else:
        # Still running — show live progress and cancel button
        progress_msgs = list(bg.get("progress", []))
        with st.status("🔄 Running analysis…", expanded=True, state="running"):
            for msg in progress_msgs:
                st.write(msg)
        if st.button("⏹ Cancel", key="cancel_eval_btn"):
            ev = st.session_state.eval_cancel_event
            if ev:
                ev.set()
            st.session_state.eval_running = False
            st.info("Cancelling… results will not be shown.")
            st.rerun()
        time.sleep(1)
        st.rerun()


# ── Prompt input ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card" style="animation:fadeUp 0.5s 0.1s both;">
  <div class="prompt-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <rect x="2" y="2" width="10" height="10" rx="2" stroke="rgba(255,255,255,0.4)" stroke-width="1.3"/>
      <path d="M4.5 5h5M4.5 7.5h3" stroke="rgba(255,255,255,0.4)" stroke-width="1.3" stroke-linecap="round"/>
    </svg>
    <span class="card-label-accent">Your Prompt</span>
  </div>
""", unsafe_allow_html=True)

# Key changes with counter force-resets the widget when Clear is clicked
prompt = st.text_area(
    "prompt_input",
    key=f"prompt_area_{st.session_state.prompt_clear_counter}",
    height=180,
    placeholder="Paste your LLM prompt here…",
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

col_btn, col_clear, col_hint = st.columns([1, 0.6, 4])
with col_btn:
    evaluate_clicked = st.button(
        "✨ Analyze Prompt", type="primary",
        use_container_width=True,
        disabled=st.session_state.eval_running,
    )
with col_clear:
    clear_clicked = st.button(
        "🗑 Clear", use_container_width=True,
        help="Clear prompt and all results",
        disabled=st.session_state.eval_running,
    )
with col_hint:
    st.markdown(
        "<p style='color:#94a3b8;font-size:13px;padding-top:10px;'>"
        "Evaluates across 8 dimensions: Clarity · Role · Format · Context · Constraints · Tone · Bias · Toxicity"
        "</p>",
        unsafe_allow_html=True,
    )

if clear_clicked:
    st.session_state.prompt_clear_counter += 1
    for key in [
        "evaluation", "original_prompt", "fix_result",
        "fix_evaluation", "variant_evaluations", "stress_test_result",
        "hallucination_result", "fix_validate_result",
    ]:
        st.session_state[key] = None if key != "original_prompt" else ""
    st.rerun()

if evaluate_clicked and not st.session_state.eval_running:
    if not prompt.strip():
        st.error("Please enter a prompt before analyzing.")
    else:
        _p = prompt.strip()
        st.session_state._pending_prompt = _p
        # Reset prior results
        for key in ["fix_result", "fix_evaluation", "fix_validate_result",
                    "variant_evaluations", "stress_test_result", "hallucination_result"]:
            st.session_state[key] = None

        cancel_ev = threading.Event()
        bg_state: dict = {
            "progress": [], "done": False, "error": None, "cancelled": False,
            "evaluation": None, "stress_result": None, "hallucination_result": None,
            "fix_result": None, "fix_validate_result": None,
        }
        st.session_state.eval_cancel_event = cancel_ev
        st.session_state.eval_bg_state = bg_state
        st.session_state.eval_running = True

        threading.Thread(
            target=_run_pipeline_bg,
            args=(_p, bg_state, cancel_ev,
                  _auto_stress, _auto_hallucination,
                  _auto_fix, _auto_eval_improvement, _attack_count),
            daemon=True,
        ).start()
        st.rerun()


# ── Scorecard ─────────────────────────────────────────────────────────────────
if st.session_state.evaluation:
    dims = st.session_state.evaluation.get("dimensions", [])
    avg_score = sum(d["score"] for d in dims) / len(dims) if dims else 0

    render_score_overview(dims)
    render_scorecard_details(dims)

    # ── Advanced features ─────────────────────────────────────────────────────
    stress_clicked = False
    hallucination_clicked = False

    if not _auto_stress or not _auto_hallucination:
        adv_cols = st.columns([1.5, 1.8, 4])
        with adv_cols[0]:
            if not _auto_stress:
                stress_clicked = st.button(
                    "🔴 Run Stress Test",
                    key="stress_test_btn",
                    use_container_width=True,
                )
        with adv_cols[1]:
            if not _auto_hallucination:
                hallucination_clicked = st.button(
                    "🧠 Hallucination Risk",
                    key="hallucination_btn",
                    use_container_width=True,
                )

    if _auto_stress and not st.session_state.stress_test_result:
        stress_clicked = True
    if _auto_hallucination and not st.session_state.hallucination_result:
        hallucination_clicked = True

    if stress_clicked:
        with st.status("Running stress test...", expanded=True) as status:
            try:
                st.write(f"⏳ Generating {_attack_count} adversarial attacks...")
                for i in range(1, _attack_count + 1):
                    st.write(f"⏳ Testing attack {i}/{_attack_count}...")
                result = call_stress_test(st.session_state.original_prompt, _attack_count)
                st.session_state.stress_test_result = result
                st.write(f"✅ Vulnerability score: {result['vulnerability_score']}/10")
                status.update(
                    label=f"🔴 Stress Test complete — vulnerability {result['vulnerability_score']}/10",
                    state="complete", expanded=False,
                )
                st.rerun()
            except Exception as e:
                status.update(label="❌ Stress test failed", state="error", expanded=False)
                st.error(f"Stress test error: {e}")

    if hallucination_clicked:
        with st.status("Checking hallucination risk...", expanded=True) as status:
            try:
                st.write("⏳ Generating sample output from prompt...")
                st.write("⏳ Analysing hallucination risk...")
                result = call_hallucination_check(st.session_state.original_prompt)
                st.session_state.hallucination_result = result
                st.write(f"✅ Hallucination score: {result['hallucination_score']}/10")
                status.update(
                    label=f"🧠 Hallucination check complete — {result['verdict']}",
                    state="complete", expanded=False,
                )
                st.rerun()
            except Exception as e:
                status.update(label="❌ Check failed", state="error", expanded=False)
                st.error(f"Hallucination check error: {e}")

    if st.session_state.stress_test_result:
        sr = st.session_state.stress_test_result
        v_score = sr["vulnerability_score"]
        v_tc = "#4ade80" if v_score >= 7 else ("#fbbf24" if v_score >= 4 else "#f87171")
        v_bg = "rgba(22,163,74,0.12)" if v_score >= 7 else ("rgba(217,119,6,0.12)" if v_score >= 4 else "rgba(220,38,38,0.12)")
        st.markdown(f"""
<div class="result-tile">
  <div class="result-tile-header">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M8 2L14 6v5L8 14 2 11V6L8 2z" stroke="{v_tc}" stroke-width="1.5" stroke-linejoin="round"/>
      <path d="M8 7v2.5l1.5 1" stroke="{v_tc}" stroke-width="1.4" stroke-linecap="round"/>
    </svg>
    <span class="result-tile-title">Stress Test Results</span>
    <span class="score-badge-pill" style="background:{v_bg};color:{v_tc};border:1px solid {v_tc}33;">
      Robustness {v_score}/10
    </span>
  </div>
""", unsafe_allow_html=True)
        for attack in sr["attacks"]:
            label = "Broke intent" if attack["verdict"] == "PASS" else "Intent preserved"
            icon_col = "#f87171" if attack["verdict"] == "PASS" else "#4ade80"
            with st.expander(f"`{attack['attack_type']}` — {label}"):
                st.markdown(f"**Attack input:** {attack['input']}")
                st.markdown(f"**Reason:** {attack['reason']}")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.hallucination_result:
        hr = st.session_state.hallucination_result
        h_tc = "#4ade80" if hr["hallucination_score"] >= 7 else ("#fbbf24" if hr["hallucination_score"] >= 4 else "#f87171")
        h_bg = "rgba(22,163,74,0.12)" if hr["hallucination_score"] >= 7 else ("rgba(217,119,6,0.12)" if hr["hallucination_score"] >= 4 else "rgba(220,38,38,0.12)")
        st.markdown(f"""
<div class="result-tile">
  <div class="result-tile-header">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M8 3l5 8.66H3L8 3z" stroke="{h_tc}" stroke-width="1.5" stroke-linejoin="round"/>
      <path d="M8 8v2M8 11.5v.5" stroke="{h_tc}" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    <span class="result-tile-title">Hallucination Risk</span>
    <span class="score-badge-pill" style="background:{h_bg};color:{h_tc};border:1px solid {h_tc}33;">
      {hr['verdict']} ({hr['hallucination_score']}/10)
    </span>
  </div>
  <p style="color:rgba(255,255,255,0.4);font-size:13px;margin:4px 0 10px;">{hr['reason']}</p>
</div>
""", unsafe_allow_html=True)
        with st.expander("View sample output used for analysis"):
            st.text(hr["sample_output"])

    # ── Download report (after all analysis tiles) ────────────────────────────
    report_text = build_scorecard_report(
        st.session_state.evaluation,
        st.session_state.original_prompt,
        stress_result=st.session_state.stress_test_result,
        hallucination_result=st.session_state.hallucination_result,
    )
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    _col_dl, _ = st.columns([2, 5])
    with _col_dl:
        st.download_button(
            label="⬇ Download Evaluation Report",
            data=report_text.encode("utf-8"),
            file_name=f"pef_evaluation_{ts}.txt",
            mime="text/plain",
            use_container_width=True,
            help="Includes scorecard, stress test results, and hallucination risk if run",
        )

    # ── Fix section ───────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:24px 0;'>", unsafe_allow_html=True)
    st.markdown('<div class="fix-section-title">Fix Your Prompt</div>', unsafe_allow_html=True)

    fix_mode = st.radio(
        "fix_mode_radio",
        options=["single", "variants"],
        format_func=lambda x: "⚡ Single best fix" if x == "single" else "🔀 3 variants to compare",
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.fix_mode = fix_mode

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    fix_clicked = st.button("🔧 Fix Prompt", type="primary")

    if fix_clicked:
        with st.status("Improving your prompt...", expanded=True) as status:
            try:
                st.write("⏳ Generating improved prompt...")
                result = call_fix(
                    st.session_state.original_prompt,
                    st.session_state.evaluation,
                    fix_mode,
                )
                st.write("✅ Improved prompt generated")
                st.session_state.fix_result = result
                st.session_state.fix_evaluation = None
                st.session_state.fix_validate_result = None
                st.session_state.variant_evaluations = None
                status.update(label="✅ Prompt improved", state="complete", expanded=False)
            except httpx.HTTPStatusError as e:
                try:
                    detail = e.response.json().get("detail", e.response.text)
                except Exception:
                    detail = e.response.text
                status.update(label="❌ Fix failed", state="error", expanded=False)
                st.error(f"Error {e.response.status_code}: {detail}")
            except Exception as e:
                status.update(label="❌ Fix failed", state="error", expanded=False)
                st.error(f"Unexpected error: {e}")

    # ── Improved Prompt ───────────────────────────────────────────────────────
    if st.session_state.fix_result:
        fix_result = st.session_state.fix_result
        st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:24px 0;'>", unsafe_allow_html=True)
        st.markdown('<div class="fix-section-title">Improved Prompt</div>', unsafe_allow_html=True)

        eval_improvement: bool = False
        if fix_result.get("fixed_prompt"):
            fixed_text = st.text_area(
                "fixed_prompt_area",
                value=fix_result["fixed_prompt"],
                height=200,
                label_visibility="collapsed",
            )
            col_dl, col_ev, col_pad = st.columns([1.2, 1.8, 4])
            with col_dl:
                ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="⬇ Download",
                    data=fixed_text.encode("utf-8"),
                    file_name=f"improved_prompt_{ts}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with col_ev:
                if not st.session_state.fix_evaluation:
                    eval_improvement = st.button(
                        "📊 Evaluate Improvement",
                        key="eval_single",
                        use_container_width=True,
                    )
                else:
                    eval_improvement = False

            # Validate improvement with step-wise progress + regression guard
            if eval_improvement:
                with st.status("Validating improvement...", expanded=True) as status:
                    try:
                        st.write("⏳ Running G-Eval on improved prompt...")
                        validate_result = call_fix_validate(
                            st.session_state.original_prompt,
                            fixed_text,
                            st.session_state.evaluation,
                        )
                        post_dims = validate_result["post_eval"]["dimensions"]
                        for d in post_dims[:6]:
                            st.write(f"✅ G-Eval — {d['name']} ({d['score']}/10)")
                        st.write("✅ Bias & Toxicity checked")
                        st.session_state.fix_evaluation = validate_result["post_eval"]
                        st.session_state.fix_validate_result = validate_result
                        status.update(label="✅ Validation complete", state="complete", expanded=False)
                        st.rerun()
                    except httpx.HTTPStatusError as e:
                        try:
                            detail = e.response.json().get("detail", e.response.text)
                        except Exception:
                            detail = e.response.text
                        status.update(label="❌ Validation failed", state="error", expanded=False)
                        st.error(f"Error {e.response.status_code}: {detail}")
                    except Exception as e:
                        status.update(label="❌ Validation failed", state="error", expanded=False)
                        st.error(f"Unexpected error: {e}")

            # ── Regenerate with Feedback ──────────────────────────────────────
            with st.expander("🔄 Not happy with the result? Regenerate with your feedback"):
                st.markdown(
                    "<p style='color:#64748b;font-size:13px;margin:0 0 10px;'>"
                    "Describe what you'd like changed and the prompt will be rewritten accordingly.</p>",
                    unsafe_allow_html=True,
                )
                regen_feedback = st.text_area(
                    "Your feedback",
                    height=100,
                    placeholder="e.g. 'Make it more concise', 'Use a friendlier tone', 'Add a JSON output format requirement', 'Focus only on Python'…",
                    key="regen_fb_single",
                )
                regen_clicked = st.button(
                    "🔄 Regenerate Prompt",
                    type="primary",
                    key="regen_single_btn",
                )

            if regen_clicked:
                if not regen_feedback.strip():
                    st.warning("Enter feedback before regenerating.")
                else:
                    with st.status("Regenerating with your feedback...", expanded=True) as status:
                        try:
                            st.write("⏳ Applying feedback...")
                            result = call_refine(
                                st.session_state.original_prompt,
                                fixed_text,
                                st.session_state.evaluation,
                                regen_feedback.strip(),
                                "single",
                            )
                            st.write("✅ Prompt regenerated")
                            st.session_state.fix_result = result
                            st.session_state.fix_evaluation = None
                            st.session_state.fix_validate_result = None
                            status.update(label="✅ Regeneration complete", state="complete", expanded=False)
                            st.rerun()
                        except httpx.HTTPStatusError as e:
                            try:
                                detail = e.response.json().get("detail", e.response.text)
                            except Exception:
                                detail = e.response.text
                            status.update(label="❌ Regeneration failed", state="error", expanded=False)
                            st.error(f"Error {e.response.status_code}: {detail}")
                        except Exception as e:
                            status.update(label="❌ Regeneration failed", state="error", expanded=False)
                            st.error(f"Unexpected error: {e}")

            if st.session_state.fix_evaluation:
                render_comparison(st.session_state.evaluation, st.session_state.fix_evaluation)

                if st.session_state.fix_validate_result:
                    vr = st.session_state.fix_validate_result
                    if vr.get("regression_warnings"):
                        warns = ", ".join(
                            f"{w['dimension']} ({w['original_score']}→{w['fixed_score']})"
                            for w in vr["regression_warnings"]
                        )
                        st.warning(f"⚠️ Some dimensions scored lower after fixing: {warns}. Review before using.")
                    if vr.get("safety_warnings"):
                        sw = ", ".join(vr["safety_warnings"])
                        st.error(f"🔴 Safety concern detected in improved prompt: {sw}. Review carefully.")

        else:
            variants = fix_result.get("variants", [])
            variant_evals = st.session_state.variant_evaluations or [None] * len(variants)
            tabs = st.tabs([f"Variant {i + 1}" for i in range(len(variants))])
            for i, (tab, v) in enumerate(zip(tabs, variants)):
                with tab:
                    variant_text = st.text_area(
                        f"Variant {i + 1}",
                        value=v,
                        height=200,
                        key=f"variant_area_{i}",
                        label_visibility="collapsed",
                    )
                    col_dl, col_ev, col_pad = st.columns([1.2, 1.8, 4])
                    with col_dl:
                        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                        st.download_button(
                            label="⬇ Download",
                            data=variant_text.encode("utf-8"),
                            file_name=f"improved_prompt_v{i+1}_{ts}.txt",
                            mime="text/plain",
                            use_container_width=True,
                            key=f"dl_variant_{i}",
                        )
                    with col_ev:
                        if i >= len(variant_evals) or not variant_evals[i]:
                            eval_v = st.button(
                                "📊 Evaluate Improvement",
                                key=f"eval_variant_{i}",
                                use_container_width=True,
                            )
                        else:
                            eval_v = False

                    # Spinner outside columns to avoid layout duplication
                    if eval_v:
                        with st.spinner(f"Evaluating Variant {i + 1}…"):
                            try:
                                ev = call_evaluate(variant_text)
                                evals: List[Optional[dict]] = list(variant_evals)
                                while len(evals) <= i:
                                    evals.append(None)
                                evals[i] = ev
                                st.session_state.variant_evaluations = evals
                                st.rerun()
                            except httpx.HTTPStatusError as e:
                                try:
                                    detail = e.response.json().get("detail", e.response.text)
                                except Exception:
                                    detail = e.response.text
                                st.error(f"Error {e.response.status_code}: {detail}")
                            except Exception as e:
                                st.error(f"Unexpected error: {e}")

                    v_eval = variant_evals[i] if i < len(variant_evals) else None
                    if v_eval is not None:
                        render_comparison(st.session_state.evaluation, v_eval)

                    # ── Regenerate with Feedback (variants) ──────────────────
                    with st.expander(f"🔄 Not happy with Variant {i + 1}? Regenerate with your feedback"):
                        st.markdown(
                            "<p style='color:#64748b;font-size:13px;margin:0 0 10px;'>"
                            "Describe what you'd like changed and this variant will be rewritten accordingly.</p>",
                            unsafe_allow_html=True,
                        )
                        vregen_feedback = st.text_area(
                            "Your feedback",
                            height=100,
                            placeholder="e.g. 'Make it shorter', 'Use bullet points for output', 'Add error handling instructions'…",
                            key=f"regen_fb_v{i}",
                        )
                        vregen_clicked = st.button(
                            "🔄 Regenerate Variant",
                            type="primary",
                            key=f"regen_v{i}_btn",
                        )

                    if vregen_clicked:
                        if not vregen_feedback.strip():
                            st.warning("Enter feedback before regenerating.")
                        else:
                            with st.spinner(f"Regenerating Variant {i + 1}…"):
                                try:
                                    result = call_refine(
                                        st.session_state.original_prompt,
                                        variant_text,
                                        st.session_state.evaluation,
                                        vregen_feedback.strip(),
                                        "single",
                                    )
                                    new_variants = list(variants)
                                    new_variants[i] = result.get("fixed_prompt", variant_text)
                                    st.session_state.fix_result = {"variants": new_variants}
                                    new_evals: List[Optional[dict]] = list(variant_evals)
                                    if i < len(new_evals):
                                        new_evals[i] = None
                                    st.session_state.variant_evaluations = new_evals
                                    st.rerun()
                                except httpx.HTTPStatusError as e:
                                    try:
                                        detail = e.response.json().get("detail", e.response.text)
                                    except Exception:
                                        detail = e.response.text
                                    st.error(f"Error {e.response.status_code}: {detail}")
                                except Exception as e:
                                    st.error(f"Unexpected error: {e}")

st.markdown(nav_close(), unsafe_allow_html=True)
