import streamlit as st

st.set_page_config(
    page_title="Prompt Evaluation Framework",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp, .stMarkdown, button, input, textarea, label {
    font-family: 'Inter', sans-serif !important;
}

.stApp { background-color: #f8fafc; color: #1e293b; }
.main .block-container { padding-top: 1.5rem; max-width: 1100px; }
#MainMenu, footer { visibility: hidden; }

p, li, span, div, td, th { color: #1e293b; }
.stMarkdown p, .stMarkdown li, .stMarkdown span { color: #1e293b !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color: #1e293b !important; }

h1 { color: #1e293b !important; font-weight: 700 !important; }
h2, h3 { color: #334155 !important; font-weight: 600 !important; }

hr { border-color: #e2e8f0 !important; margin: 1.25rem 0 !important; }

.hero-banner {
    background: linear-gradient(135deg, #FF3621 0%, #e02d1a 100%);
    border-radius: 16px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}
.hero-banner h1 {
    color: white !important;
    font-size: 2.4rem !important;
    margin: 0 0 0.6rem !important;
    letter-spacing: -0.02em;
}
.hero-banner p {
    color: rgba(255,255,255,0.88);
    font-size: 1.1rem;
    margin: 0;
    line-height: 1.6;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.nav-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    margin-bottom: 2rem;
}
.nav-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.5rem 1.5rem 1.25rem;
    text-align: center;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.nav-card:hover {
    border-color: #ffb3a7;
    box-shadow: 0 4px 16px rgba(255,54,33,0.1);
}
.nav-card .icon { font-size: 2rem; margin-bottom: 0.6rem; }
.nav-card h3 {
    color: #1e293b !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin: 0 0 0.4rem !important;
}
.nav-card p { color: #64748b; font-size: 0.85rem; margin: 0; line-height: 1.4; }

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FF3621 0%, #cc2c1a 100%) !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(255,54,33,0.3) !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1.5px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * { color: #334155 !important; }

/* Brand header strip */
[data-testid="stSidebar"]::before {
    content: "PEF";
    display: block;
    background: linear-gradient(135deg, #FF3621 0%, #cc2c1a 100%);
    color: white !important;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.1em;
    padding: 1rem 1.25rem 0.85rem;
    margin-bottom: 0.25rem;
}

[data-testid="stSidebarNav"] { padding: 0.5rem 0 !important; }

[data-testid="stSidebarNavLink"] {
    border-radius: 8px !important;
    margin: 2px 8px !important;
    padding: 0.55rem 0.9rem !important;
    color: #475569 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    transition: background 0.15s, color 0.15s !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: #fff5f3 !important;
    color: #FF3621 !important;
}
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: #fff5f3 !important;
    color: #FF3621 !important;
    font-weight: 600 !important;
    border-left: 3px solid #FF3621 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-banner">
  <h1>🔍 Prompt Evaluation Framework</h1>
  <p>AI-powered analysis and improvement for your LLM prompts — instant scoring, detailed feedback, and automatic rewrites.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav-grid">
  <div class="nav-card">
    <div class="icon">📖</div>
    <h3>Get Started</h3>
    <p>Learn how to use the tool, understand the 8 DeepEval dimensions, and see example prompts.</p>
  </div>
  <div class="nav-card">
    <div class="icon">🧪</div>
    <h3>Evaluate &amp; Fix</h3>
    <p>Score your prompt across 8 quality dimensions, auto-fix regressions, stress-test robustness, and check hallucination risk.</p>
  </div>
  <div class="nav-card">
    <div class="icon">⚙️</div>
    <h3>Settings</h3>
    <p>Configure your Databricks credentials and set evaluation defaults (auto-checks, stress test count, fix passes).</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:white;border:1.5px solid #e2e8f0;border-radius:14px;padding:1.5rem 1.75rem;color:#64748b;font-size:0.9rem;line-height:1.6;">
  <strong style="color:#1e293b;">Quick start:</strong> Head to <strong>Settings</strong> to configure your Databricks credentials, then go to <strong>Evaluate &amp; Fix</strong> to analyze your first prompt.
</div>
""", unsafe_allow_html=True)
