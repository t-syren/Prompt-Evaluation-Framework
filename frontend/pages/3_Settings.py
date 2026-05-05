import os
from typing import Optional
import httpx
import streamlit as st

st.set_page_config(page_title="Settings — PEF", page_icon="⚙️", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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
p, li, span, div, td, th { color: #1e293b; }
.stMarkdown p, .stMarkdown li, .stMarkdown span { color: #1e293b !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color: #1e293b !important; }
.stCaption, [data-testid="stCaptionContainer"] { color: #64748b !important; }

h1 { color: #1e293b !important; font-weight: 700 !important; }
h2, h3 { color: #334155 !important; font-weight: 600 !important; }

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FF3621 0%, #cc2c1a 100%) !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; letter-spacing: 0.01em !important;
    padding: 0.5rem 1.75rem !important;
    box-shadow: 0 4px 12px rgba(255,54,33,0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(255,54,33,0.4) !important;
}

.stTextInput > div > div > input,
[data-testid="stTextInput"] input {
    border-radius: 8px !important; border: 1.5px solid #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important; font-size: 14px !important;
    background: white !important; color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #FF3621 !important;
    box-shadow: 0 0 0 3px rgba(255,54,33,0.1) !important;
}
.stTextInput label, [data-testid="stWidgetLabel"] {
    color: #334155 !important;
}

.stAlert { border-radius: 10px !important; }
hr { border-color: #e2e8f0 !important; margin: 1.25rem 0 !important; }

.hero-banner {
    background: linear-gradient(135deg, #FF3621 0%, #e02d1a 100%);
    border-radius: 16px;
    padding: 2.5rem 2.5rem 2rem;
    margin-bottom: 2rem;
    color: white;
}
.hero-banner h1 { color: white !important; font-size: 2rem !important; margin: 0 0 0.5rem !important; }
.hero-banner p { color: rgba(255,255,255,0.88); font-size: 1.05rem; margin: 0; line-height: 1.6; }

.settings-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    padding: 2rem 2.25rem;
    margin-bottom: 1.25rem;
}
.settings-card h3 {
    color: #1e293b !important;
    font-size: 1.1rem !important;
    margin: 0 0 0.35rem !important;
    font-weight: 600 !important;
}
.settings-card p {
    color: #64748b;
    font-size: 0.88rem;
    margin: 0 0 1.5rem;
    line-height: 1.5;
}

.token-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-size: 0.82rem; font-weight: 500; padding: 0.3rem 0.7rem;
    border-radius: 20px; margin-top: 0.5rem;
}
.token-badge.ok { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.token-badge.warn { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }

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


def load_current_config() -> dict:
    try:
        resp = httpx.get(f"{BACKEND_URL}/config", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}


def save_config(base_url: str, llm_url: str, token: str, defaults: Optional[dict] = None) -> bool:
    try:
        payload: dict = {
            "databricks_base_url": base_url,
            "llm_endpoint_url": llm_url,
            "api_token": token,
        }
        if defaults:
            payload.update(defaults)
        resp = httpx.post(f"{BACKEND_URL}/config", json=payload, timeout=5)
        resp.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Failed to save settings: {e}")
        return False


def save_defaults(defaults: dict) -> bool:
    try:
        current = load_current_config()
        payload = {
            "databricks_base_url": current.get("databricks_base_url", ""),
            "llm_endpoint_url": current.get("llm_endpoint_url", ""),
            "api_token": "",
        }
        payload.update(defaults)
        resp = httpx.post(f"{BACKEND_URL}/config", json=payload, timeout=5)
        resp.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Failed to save defaults: {e}")
        return False


st.markdown("""
<div class="hero-banner">
  <h1>⚙️ Settings</h1>
  <p>Configure your Databricks connection. Settings are saved to the server and persist across sessions.</p>
</div>
""", unsafe_allow_html=True)

current = load_current_config()
token_status = current.get("api_token_set", False)

st.markdown("""
<div class="settings-card">
  <h3>Databricks Connection</h3>
  <p>Enter your workspace URL, LLM serving endpoint, and personal access token below.</p>
""", unsafe_allow_html=True)

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

    if token_status:
        st.markdown('<div class="token-badge ok">✅ A token is currently saved on the server</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="token-badge warn">⚠️ No token configured yet</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Save Settings", type="primary")

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if not base_url or not llm_url:
        st.error("Databricks Base URL and LLM Endpoint URL are required.")
    elif not token and not token_status:
        st.error("API Token is required — no token is currently saved on the server.")
    else:
        # Pass empty string when token field is blank; backend will keep the existing token.
        if save_config(base_url, llm_url, token):
            st.success("✅ Settings saved successfully.")

st.markdown("""
<div class="settings-card" style="margin-top:1rem;">
  <h3>Where to find these values</h3>
  <p style="margin:0;">
    <strong>Databricks Base URL</strong> — your workspace URL, e.g. <code>https://adb-xxxx.azuredatabricks.net</code><br><br>
    <strong>LLM Endpoint URL</strong> — the full serving endpoint path, found in
    <em>Machine Learning → Serving → &lt;your endpoint&gt; → Query endpoint</em><br><br>
    <strong>API Token</strong> — a Personal Access Token from
    <em>User Settings → Developer → Access tokens</em>
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="settings-card" style="margin-top:1rem;">
  <h3>Evaluation Defaults</h3>
  <p>Control which automated checks run after evaluating or fixing a prompt.</p>
""", unsafe_allow_html=True)

with st.form("defaults_form"):
    col1, col2 = st.columns(2)

    st.markdown(
        "<p style='font-size:0.82rem;color:#64748b;margin:0 0 0.75rem;'>"
        "When <strong>Auto-fix</strong> and <strong>Auto-evaluate improvement</strong> are both on, "
        "clicking Analyse runs the full pipeline automatically: "
        "Analyse → Stress test → Hallucination check → Fix → Evaluate fix.</p>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)

    with col1:
        auto_eval = st.toggle(
            "Auto-evaluate after fixing",
            value=current.get("auto_evaluate_after_fix", True),
            help="Re-run the full DeepEval scorecard automatically after every fix.",
        )
        auto_stress = st.toggle(
            "Auto-run stress test",
            value=current.get("auto_stress_test", False),
            help="Run adversarial attack tests automatically after evaluation.",
        )
        auto_hallucination = st.toggle(
            "Auto-run hallucination check",
            value=current.get("auto_hallucination_check", False),
            help="Run hallucination risk check automatically after evaluation.",
        )
        auto_fix = st.toggle(
            "Auto-fix prompt",
            value=current.get("auto_fix_prompt", False),
            help="Automatically generate an improved prompt after evaluation completes.",
        )
        auto_eval_improvement = st.toggle(
            "Auto-evaluate improvement",
            value=current.get("auto_evaluate_improvement", False),
            help="Automatically validate the fixed prompt (regression + safety) after fixing.",
        )

    with col2:
        attack_count = st.selectbox(
            "Stress test attack count",
            options=[3, 5, 10],
            index=[3, 5, 10].index(current.get("stress_test_attack_count", 5)),
            help="Number of adversarial attacks to generate per stress test run.",
        )
        fix_passes = st.selectbox(
            "Iterative fix passes",
            options=[1, 2, 3],
            index=[1, 2, 3].index(current.get("iterative_fix_passes", 2)),
            help="How many improvement passes the fixer makes when refining a prompt.",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    defaults_submitted = st.form_submit_button("Save Defaults", type="primary")

st.markdown("</div>", unsafe_allow_html=True)

if defaults_submitted:
    defaults_payload = {
        "auto_evaluate_after_fix": auto_eval,
        "auto_stress_test": auto_stress,
        "auto_hallucination_check": auto_hallucination,
        "auto_fix_prompt": auto_fix,
        "auto_evaluate_improvement": auto_eval_improvement,
        "stress_test_attack_count": attack_count,
        "iterative_fix_passes": fix_passes,
    }
    if save_defaults(defaults_payload):
        st.success("✅ Evaluation defaults saved.")
