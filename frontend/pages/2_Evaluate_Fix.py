import os
import time
import threading
import httpx
import streamlit as st
import streamlit.components.v1 as st_components
from datetime import datetime, timezone

st.set_page_config(page_title="Evaluate & Fix — PEF", page_icon="🔍", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ── Global styles ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp, .stMarkdown, button, input, textarea, label {
    font-family: 'Inter', sans-serif !important;
}

.stApp { background-color: #f8fafc; color: #1e293b; }
.main .block-container { padding-top: 1.5rem; max-width: 1100px; }
#MainMenu, footer { visibility: hidden; }

/* General text — overrides dark-mode theme inheritance */
p, li, span, div, td, th, caption { color: #1e293b; }
.stMarkdown p, .stMarkdown li, .stMarkdown span { color: #1e293b !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color: #1e293b !important; }

/* Headings */
h1 { color: #1e293b !important; font-weight: 700 !important; }
h2, h3 { color: #334155 !important; font-weight: 600 !important; }

/* Primary button — Databricks orange */
.stButton > button[kind="primary"] {
    background: #FF3621 !important;
    border: none !important; border-radius: 8px !important;
    color: white !important; font-weight: 600 !important;
    letter-spacing: 0.01em !important; padding: 0.5rem 1.75rem !important;
    box-shadow: 0 4px 12px rgba(255,54,33,0.35) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    background: #e02d1a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(255,54,33,0.45) !important;
}

/* Secondary button — dark/black */
.stButton > button:not([kind="primary"]) {
    border-radius: 8px !important; font-weight: 500 !important;
    border: none !important;
    background: #1e293b !important; color: white !important;
    transition: background 0.2s !important;
}
.stButton > button:not([kind="primary"]):hover { background: #334155 !important; }
.stButton > button:not([kind="primary"]) *,
.stButton > button:not([kind="primary"]) p {
    color: white !important; -webkit-text-fill-color: white !important;
}

/* Download button — dark/black */
.stDownloadButton > button,
[data-testid="stDownloadButton"] button {
    border-radius: 8px !important; font-weight: 500 !important;
    border: none !important; background: #1e293b !important;
    color: white !important; -webkit-text-fill-color: white !important;
    transition: background 0.2s !important;
}
.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] button:hover { background: #334155 !important; }
.stDownloadButton > button *,
.stDownloadButton > button p,
[data-testid="stDownloadButton"] button *,
[data-testid="stDownloadButton"] button p {
    color: white !important; -webkit-text-fill-color: white !important;
}

/* Text area */
.stTextArea textarea {
    border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important;
    font-family: 'Inter', monospace !important; font-size: 14px !important;
    background: white !important; color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    line-height: 1.6 !important; transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #FF3621 !important;
    box-shadow: 0 0 0 3px rgba(255,54,33,0.12) !important;
}
.stTextArea textarea::placeholder { color: #94a3b8 !important; -webkit-text-fill-color: #94a3b8 !important; }

/* Labels */
.stTextArea label, .stTextInput label, .stRadio label,
[data-testid="stWidgetLabel"] { color: #334155 !important; }

/* Radio */
.stRadio > label { font-weight: 600 !important; color: #334155 !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #334155 !important; }

/* Expander */
details { border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important; background: white !important; margin-bottom: 6px !important; }
details * { color: #1e293b !important; }
summary { font-weight: 500 !important; padding: 0.6rem 1rem !important; color: #334155 !important; }

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #FF3621, #ff6b52) !important;
    border-radius: 10px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] { font-weight: 500 !important; font-size: 0.9rem !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #FF3621 !important; }
.stTabs [aria-selected="true"] { color: #FF3621 !important; }

/* Alerts */
.stAlert { border-radius: 10px !important; }

/* Divider */
hr { border-color: #e2e8f0 !important; margin: 1.25rem 0 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #FF3621 !important; }

/* ── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1.5px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * { color: #334155 !important; }
[data-testid="stSidebar"]::before {
    content: "PEF";
    display: block;
    background: linear-gradient(135deg, #FF3621 0%, #cc2c1a 100%);
    color: white !important;
    font-family: 'Inter', sans-serif;
    font-weight: 700; font-size: 1rem; letter-spacing: 0.1em;
    padding: 1rem 1.25rem 0.85rem; margin-bottom: 0.25rem;
}
[data-testid="stSidebarNav"] { padding: 0.5rem 0 !important; }
[data-testid="stSidebarNavLink"] {
    border-radius: 8px !important; margin: 2px 8px !important;
    padding: 0.55rem 0.9rem !important; color: #475569 !important;
    font-weight: 500 !important; font-size: 0.88rem !important;
    transition: background 0.15s, color 0.15s !important;
}
[data-testid="stSidebarNavLink"]:hover { background: #fff5f3 !important; color: #FF3621 !important; }
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: #fff5f3 !important; color: #FF3621 !important;
    font-weight: 600 !important; border-left: 3px solid #FF3621 !important;
}
</style>
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
def score_color(score: int) -> tuple[str, str, str]:
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
    """Compact score card grid — one card per dimension."""
    cols = st.columns(len(dimensions))
    for col, dim in zip(cols, dimensions):
        score = dim["score"]
        tc, bg, border = score_color(score)
        short = dim["name"].split(" & ")[0].split(" / ")[0]
        col.markdown(f"""
        <div style="background:{bg};border:1.5px solid {border};border-radius:14px;
                    padding:18px 10px;text-align:center;">
            <div style="font-size:30px;font-weight:700;color:{tc}!important;line-height:1;">{score}</div>
            <div style="font-size:10px;color:#94a3b8!important;font-weight:600;
                        text-transform:uppercase;letter-spacing:0.05em;margin-top:6px;">/10</div>
            <div style="font-size:12px;color:#475569!important;font-weight:500;
                        margin-top:8px;line-height:1.3;">{short}</div>
        </div>
        """, unsafe_allow_html=True)


def render_scorecard_details(dimensions: list):
    """Expandable detail rows per dimension with progress bar and G-Eval reasoning."""
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    for dim in dimensions:
        score = dim["score"]
        emoji = score_emoji(score)
        with st.expander(f"{emoji} **{dim['name']}** — {score}/10"):
            st.progress(score / 10)
            if dim.get("reasoning"):
                st.markdown(f"**🧠 Analysis**\n\n{dim['reasoning']}")
                st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                if dim["issues"]:
                    st.markdown("**⚠️ Issues found**")
                    for issue in dim["issues"]:
                        st.markdown(f"- {issue}")
                elif score < 7:
                    if score < 4:
                        st.markdown("**🔴 Critical — needs significant improvement**")
                    else:
                        st.markdown("**⚠️ Below target — review analysis above**")
                else:
                    st.markdown("**✅ No issues found**")
            with c2:
                if dim["suggestions"]:
                    st.markdown("**💡 Suggestions**")
                    for s in dim["suggestions"]:
                        st.markdown(f"- {s}")
                elif score < 7:
                    st.markdown("**💡 See analysis above for improvement guidance**")
                else:
                    st.markdown("**✅ Looks good**")


def render_comparison(original_eval: dict, fixed_eval: dict):
    """Before/after scorecard comparison table."""
    orig_dims = {d["name"]: d["score"] for d in original_eval.get("dimensions", [])}
    fix_dims  = {d["name"]: d["score"] for d in fixed_eval.get("dimensions", [])}

    orig_avg = sum(orig_dims.values()) / len(orig_dims) if orig_dims else 0
    fix_avg  = sum(fix_dims.values())  / len(fix_dims)  if fix_dims  else 0
    total_d  = fix_avg - orig_avg

    td_color = "#16a34a" if total_d > 0 else ("#dc2626" if total_d < 0 else "#64748b")
    td_bg    = "#f0fdf4" if total_d > 0 else ("#fef2f2" if total_d < 0 else "#f1f5f9")
    td_sign  = "+" if total_d > 0 else ""
    td_arrow = "↑" if total_d > 0 else ("↓" if total_d < 0 else "→")

    rows = ""
    for name in orig_dims:
        o = orig_dims.get(name, 0)
        f = fix_dims.get(name, o)
        d = f - o
        o_tc, o_bg, o_brd = score_color(o)
        f_tc, f_bg, f_brd = score_color(f)
        dc     = "#16a34a" if d > 0 else ("#dc2626" if d < 0 else "#94a3b8")
        dsign  = "+" if d > 0 else ""
        darrow = "↑" if d > 0 else ("↓" if d < 0 else "—")
        rows += (
            f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr 0.7fr;gap:8px;align-items:center;padding:7px 0;border-bottom:1px solid #f1f5f9;">'
            f'<span style="font-size:13px;color:#334155!important;font-weight:500;">{name}</span>'
            f'<div style="background:{o_bg};border:1px solid {o_brd};border-radius:6px;text-align:center;padding:3px 6px;">'
            f'<span style="font-size:15px;font-weight:700;color:{o_tc}!important;">{o}</span>'
            f'<span style="font-size:11px;color:#94a3b8!important;">/10</span></div>'
            f'<div style="background:{f_bg};border:1px solid {f_brd};border-radius:6px;text-align:center;padding:3px 6px;">'
            f'<span style="font-size:15px;font-weight:700;color:{f_tc}!important;">{f}</span>'
            f'<span style="font-size:11px;color:#94a3b8!important;">/10</span></div>'
            f'<div style="text-align:center;"><span style="font-size:13px;font-weight:700;color:{dc}!important;">{darrow} {dsign}{d}</span></div>'
            f'</div>'
        )

    st.markdown(f"""
    <div style="margin-top:20px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
        <span style="font-size:16px;font-weight:700;color:#1e293b!important;">📈 Score Comparison</span>
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <span style="font-size:13px;color:#64748b!important;">Before: <strong style="color:#1e293b!important;">{orig_avg:.1f}/10</strong></span>
          <span style="color:#cbd5e1!important;font-size:16px;">→</span>
          <span style="font-size:13px;color:#64748b!important;">After: <strong style="color:#1e293b!important;">{fix_avg:.1f}/10</strong></span>
          <span style="background:{td_bg};color:{td_color}!important;font-weight:700;
                       font-size:13px;padding:3px 12px;border-radius:20px;">
            {td_arrow} {td_sign}{total_d:.1f}
          </span>
        </div>
      </div>
      <div style="background:white;border:1.5px solid #e2e8f0;border-radius:12px;padding:6px 16px 2px;">
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr 0.7fr;gap:8px;
                    padding-bottom:6px;border-bottom:1.5px solid #e2e8f0;">
          <span style="font-size:11px;font-weight:600;color:#94a3b8!important;text-transform:uppercase;letter-spacing:0.05em;">Dimension</span>
          <span style="font-size:11px;font-weight:600;color:#94a3b8!important;text-transform:uppercase;letter-spacing:0.05em;text-align:center;">Before</span>
          <span style="font-size:11px;font-weight:600;color:#94a3b8!important;text-transform:uppercase;letter-spacing:0.05em;text-align:center;">After</span>
          <span style="font-size:11px;font-weight:600;color:#94a3b8!important;text-transform:uppercase;letter-spacing:0.05em;text-align:center;">Δ</span>
        </div>
        {rows}
      </div>
    </div>
    """, unsafe_allow_html=True)


def build_scorecard_report(
    evaluation: dict,
    original_prompt: str,
    stress_result: dict | None = None,
    hallucination_result: dict | None = None,
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


# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#FF3621 0%,#cc2c1a 100%);
            border-radius:16px;padding:28px 32px;margin-bottom:24px;
            box-shadow:0 8px 24px rgba(255,54,33,0.25);">
  <h1 style="color:white!important;margin:0;font-size:1.75rem;">🔍 Evaluate & Fix</h1>
  <p style="color:rgba(255,255,255,0.85);margin:8px 0 0;font-size:15px;">
    Paste any LLM prompt to get a scored evaluation across 8 quality dimensions powered by DeepEval,
    then generate an improved version, stress test it, or check hallucination risk.
  </p>
</div>
""", unsafe_allow_html=True)


# Inject scroll-to-top button into the host Streamlit page via component iframe
st_components.html("""
<script>
(function() {
    var p = window.parent.document;
    if (p.getElementById('pef-scroll-top')) return;
    var s = p.createElement('style');
    s.textContent = '#pef-scroll-top{position:fixed;bottom:1.5rem;right:1.5rem;z-index:2147483647;'
        + 'background:linear-gradient(135deg,#FF3621,#cc2c1a);color:#fff;border:none;'
        + 'border-radius:50%;width:42px;height:42px;font-size:20px;cursor:pointer;'
        + 'box-shadow:0 4px 14px rgba(255,54,33,.45);display:flex;align-items:center;'
        + 'justify-content:center;transition:opacity .2s;line-height:1}'
        + '#pef-scroll-top:hover{opacity:.8}';
    p.head.appendChild(s);
    var btn = p.createElement('button');
    btn.id = 'pef-scroll-top';
    btn.title = 'Back to top';
    btn.textContent = '↑';
    btn.onclick = function() {
        var sels = ['[data-testid="stMain"]', '.main', 'section.main',
                    '[data-testid="block-container"]', '.block-container'];
        for (var i = 0; i < sels.length; i++) {
            var el = p.querySelector(sels[i]);
            if (el && el.scrollHeight > el.clientHeight) {
                el.scrollTo({top: 0, behavior: 'smooth'});
                return;
            }
        }
        window.parent.scrollTo({top: 0, behavior: 'smooth'});
    };
    p.body.appendChild(btn);
})();
</script>
""", height=0, scrolling=False)

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
<div style="background:white;border-radius:14px;padding:20px 24px;
            border:1.5px solid #e2e8f0;box-shadow:0 1px 4px rgba(0,0,0,0.05);
            margin-bottom:16px;">
  <div style="font-size:13px;font-weight:600;color:#FF3621;
              text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">
    Your Prompt
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
    tc_avg, bg_avg, border_avg = score_color(round(avg_score))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
      <div>
        <span style="font-size:18px;font-weight:700;color:#1e293b!important;">📊 Evaluation Scorecard</span>
        <span style="font-size:13px;color:#94a3b8!important;margin-left:10px;">8 dimensions rated 1–10</span>
      </div>
      <div style="background:{bg_avg};border:1.5px solid {border_avg};border-radius:10px;
                  padding:6px 16px;text-align:center;">
        <span style="font-size:13px;color:#64748b!important;font-weight:500;">Overall </span>
        <span style="font-size:18px;font-weight:700;color:{tc_avg}!important;">{avg_score:.1f}</span>
        <span style="font-size:13px;color:#94a3b8!important;">/10</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

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
        v_tc, v_bg, v_brd = score_color(v_score)
        st.markdown(f"""
<div style="margin-top:16px;background:white;border:1.5px solid #e2e8f0;
            border-radius:14px;padding:16px 20px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
    <span style="font-size:15px;font-weight:700;color:#1e293b!important;">🔴 Stress Test Results</span>
    <span style="background:{v_bg};border:1px solid {v_brd};color:{v_tc}!important;
                 font-weight:700;font-size:13px;padding:3px 10px;border-radius:20px;">
      Robustness {v_score}/10
    </span>
  </div>
""", unsafe_allow_html=True)
        for attack in sr["attacks"]:
            label = "⚠️ Broke intent" if attack["verdict"] == "PASS" else "✅ Intent preserved"
            with st.expander(f"`{attack['attack_type']}` — {label}"):
                st.markdown(f"**Attack input:** {attack['input']}")
                st.markdown(f"**Reason:** {attack['reason']}")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.hallucination_result:
        hr = st.session_state.hallucination_result
        h_tc, h_bg, h_brd = score_color(hr["hallucination_score"])
        st.markdown(f"""
<div style="margin-top:16px;background:white;border:1.5px solid #e2e8f0;
            border-radius:14px;padding:16px 20px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
    <span style="font-size:15px;font-weight:700;color:#1e293b!important;">🧠 Hallucination Risk</span>
    <span style="background:{h_bg};border:1px solid {h_brd};color:{h_tc}!important;
                 font-weight:700;font-size:13px;padding:3px 10px;border-radius:20px;">
      {hr['verdict']} ({hr['hallucination_score']}/10)
    </span>
  </div>
  <p style="color:#64748b!important;font-size:13px;margin:4px 0 10px;">{hr['reason']}</p>
</div>
""", unsafe_allow_html=True)
        with st.expander("📄 View sample output used for analysis"):
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
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:18px;font-weight:700;color:#1e293b;margin-bottom:14px;">
      🔧 Fix Your Prompt
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:18px;font-weight:700;color:#1e293b;margin-bottom:14px;">
          ✨ Improved Prompt
        </div>
        """, unsafe_allow_html=True)

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
                                evals: list[dict | None] = list(variant_evals)
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
                                    new_evals: list[dict | None] = list(variant_evals)
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
