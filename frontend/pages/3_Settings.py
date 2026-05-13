import os
from typing import Optional
import httpx
import streamlit as st
from frontend.styles import base_css, nav_html, nav_close, inject_sidebar_killer

st.set_page_config(page_title="Settings — PEF", page_icon=None, layout="wide",
                   initial_sidebar_state="collapsed")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

inject_sidebar_killer()
st.markdown(base_css(), unsafe_allow_html=True)
st.markdown(nav_html("settings"), unsafe_allow_html=True)

st.markdown("""
<style>
.page-header { margin-bottom: 28px; animation: fadeUp 0.5s 0.05s both; }
.page-title  { font-size: 24px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.025em; margin-bottom: 6px; }
.page-sub    { font-size: 14px; color: rgba(255,255,255,0.35); }

.token-badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 600; padding: 4px 12px;
  border-radius: 20px; margin-top: 8px;
}
.token-ok   { background: rgba(22,163,74,0.12);  color: #4ade80; border: 1px solid rgba(22,163,74,0.25); }
.token-warn { background: rgba(217,119,6,0.12);  color: #fbbf24; border: 1px solid rgba(217,119,6,0.25); }

.help-card {
  background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px; padding: 16px 20px; font-size: 13px;
  color: rgba(255,255,255,0.45); line-height: 1.8;
}
.help-card strong { color: rgba(255,255,255,0.7); }
</style>

<div class="page-header anim-1">
  <div class="page-title">Settings</div>
  <div class="page-sub">Configure your Databricks connection. Settings persist across sessions.</div>
</div>
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


current = load_current_config()
token_status = current.get("api_token_set", False)

# ── Databricks Connection ──────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card anim-2">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <path d="M7 2L12 5V9L7 12L2 9V5L7 2Z" stroke="rgba(255,255,255,0.4)" stroke-width="1.4" stroke-linejoin="round"/>
    </svg>
    <span class="card-label">Databricks Connection</span>
  </div>
  <div class="glass-card-body">
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
        st.markdown('<div class="token-badge token-ok"><svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 5l2.5 2.5 3.5-4" stroke="#4ade80" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg> Token saved on server</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="token-badge token-warn"><svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M5 3v3M5 7.5v.5" stroke="#fbbf24" stroke-width="1.4" stroke-linecap="round"/></svg> No token configured</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Save Settings", type="primary")

st.markdown("</div></div>", unsafe_allow_html=True)

if submitted:
    if not base_url or not llm_url:
        st.error("Databricks Base URL and LLM Endpoint URL are required.")
    elif not token and not token_status:
        st.error("API Token is required — no token is currently saved on the server.")
    else:
        if save_config(base_url, llm_url, token):
            st.success("Settings saved successfully.")

# ── Where to find values ───────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card anim-3">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <circle cx="7" cy="7" r="5" stroke="rgba(255,255,255,0.4)" stroke-width="1.4"/>
      <path d="M7 6v4M7 4.5v.5" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    <span class="card-label">Where to find these values</span>
  </div>
  <div class="glass-card-body">
    <div class="help-card">
      <strong>Databricks Base URL</strong> — your workspace URL, e.g. <code>https://adb-xxxx.azuredatabricks.net</code><br>
      <strong>LLM Endpoint URL</strong> — the full serving endpoint path, found in <em>Machine Learning → Serving → &lt;your endpoint&gt; → Query endpoint</em><br>
      <strong>API Token</strong> — a Personal Access Token from <em>User Settings → Developer → Access tokens</em>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Evaluation Defaults ────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card anim-4">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <path d="M2 4h10M2 7h10M2 10h6" stroke="rgba(255,255,255,0.4)" stroke-width="1.4" stroke-linecap="round"/>
    </svg>
    <span class="card-label">Evaluation Defaults</span>
  </div>
  <div class="glass-card-body">
    <p style="font-size:12px;color:rgba(255,255,255,0.3);margin:0 0 16px;line-height:1.6;">
      When <strong style="color:rgba(255,255,255,0.6);">Auto-fix</strong> and <strong style="color:rgba(255,255,255,0.6);">Auto-evaluate improvement</strong> are both on,
      clicking Analyze runs the full pipeline automatically.
    </p>
""", unsafe_allow_html=True)

with st.form("defaults_form"):
    col1, col2 = st.columns(2)
    with col1:
        auto_eval = st.toggle("Auto-evaluate after fixing", value=current.get("auto_evaluate_after_fix", True),
                              help="Re-run the full DeepEval scorecard after every fix.")
        auto_stress = st.toggle("Auto-run stress test", value=current.get("auto_stress_test", False),
                                help="Run adversarial attacks automatically after evaluation.")
        auto_hallucination = st.toggle("Auto-run hallucination check", value=current.get("auto_hallucination_check", False),
                                       help="Run hallucination risk check automatically after evaluation.")
        auto_fix = st.toggle("Auto-fix prompt", value=current.get("auto_fix_prompt", False),
                             help="Automatically generate an improved prompt after evaluation.")
        auto_eval_improvement = st.toggle("Auto-evaluate improvement", value=current.get("auto_evaluate_improvement", False),
                                          help="Validate the fixed prompt (regression + safety) after fixing.")
    with col2:
        attack_count = st.selectbox("Stress test attack count", options=[3, 5, 10],
                                    index=[3, 5, 10].index(current.get("stress_test_attack_count", 5)),
                                    help="Number of adversarial attacks per stress test run.")
        fix_passes = st.selectbox("Iterative fix passes", options=[1, 2, 3],
                                  index=[1, 2, 3].index(current.get("iterative_fix_passes", 2)),
                                  help="How many improvement passes the fixer makes.")
    st.markdown("<br>", unsafe_allow_html=True)
    defaults_submitted = st.form_submit_button("Save Defaults", type="primary")

st.markdown("</div></div>", unsafe_allow_html=True)

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
        st.success("Evaluation defaults saved.")

st.markdown(nav_close(), unsafe_allow_html=True)
