import streamlit as st

st.set_page_config(page_title="Get Started — PEF", page_icon="📖", layout="wide")

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

details {
    border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important;
    background: white !important; margin-bottom: 6px !important;
}
summary { font-weight: 500 !important; padding: 0.6rem 1rem !important; }
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

.info-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}
.info-card h3 { color: #334155 !important; font-size: 1.05rem !important; margin: 0 0 0.75rem !important; }

.step-row {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    margin-bottom: 0.85rem;
}
.step-num {
    background: linear-gradient(135deg, #FF3621, #cc2c1a);
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    width: 26px; height: 26px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
.step-text { color: #475569; font-size: 0.95rem; line-height: 1.5; }
.step-text strong { color: #1e293b; }

.dim-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-top: 0.5rem;
}
.dim-item {
    background: #fff5f3;
    border: 1.5px solid #ffd5cf;
    border-radius: 10px;
    padding: 0.85rem 1rem;
}
.dim-name { font-weight: 600; color: #cc2c1a; font-size: 0.9rem; margin-bottom: 0.2rem; }
.dim-desc { color: #64748b; font-size: 0.82rem; line-height: 1.4; }

.setup-step {
    display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.6rem;
}
.setup-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.setup-text { color: #475569; font-size: 0.93rem; line-height: 1.5; }
.setup-text strong { color: #1e293b; }

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

st.markdown("""
<div class="hero-banner">
  <h1>📖 Get Started</h1>
  <p>Everything you need to know to get the most out of the Prompt Evaluation Framework.</p>
</div>
""", unsafe_allow_html=True)

# What is PEF
st.markdown("""
<div class="info-card">
  <h3>What is PEF?</h3>
  <p style="color:#475569;font-size:0.95rem;margin:0;line-height:1.6;">
    The <strong>Prompt Evaluation Framework</strong> is an AI-powered tool that analyzes any LLM prompt
    and tells you exactly what's working, what isn't, and how to improve it — instantly.
    It scores your prompt across 8 quality dimensions powered by DeepEval and can automatically rewrite it for you.
    Safety metrics (Bias &amp; Toxicity) are checked automatically on every evaluation.
  </p>
</div>
""", unsafe_allow_html=True)

# How It Works
st.markdown("""
<div class="info-card">
  <h3>How It Works</h3>
  <div class="step-row">
    <div class="step-num">1</div>
    <div class="step-text"><strong>Paste your prompt</strong> on the <em>Evaluate &amp; Fix</em> page</div>
  </div>
  <div class="step-row">
    <div class="step-num">2</div>
    <div class="step-text"><strong>Click Evaluate</strong> — DeepEval scores your prompt across 8 quality dimensions with chain-of-thought reasoning</div>
  </div>
  <div class="step-row">
    <div class="step-num">3</div>
    <div class="step-text"><strong>Review the scorecard</strong> — see AI analysis, specific issues, and improvement suggestions per dimension</div>
  </div>
  <div class="step-row">
    <div class="step-num">4</div>
    <div class="step-text"><strong>Click Fix Prompt</strong> — generate an improved version; the fixer validates regressions automatically</div>
  </div>
  <div class="step-row">
    <div class="step-num">5</div>
    <div class="step-text"><strong>Run stress test or hallucination check</strong> — probe adversarial robustness and factual accuracy</div>
  </div>
  <div class="step-row">
    <div class="step-num">6</div>
    <div class="step-text"><strong>Download or copy</strong> your improved prompt and evaluation report</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Evaluation Dimensions
st.markdown("""
<div class="info-card">
  <h3>Evaluation Dimensions (8 total, scored 1–10)</h3>
  <div class="dim-grid">
    <div class="dim-item">
      <div class="dim-name">Clarity &amp; Specificity</div>
      <div class="dim-desc">Is the prompt unambiguous and precise?</div>
    </div>
    <div class="dim-item">
      <div class="dim-name">Role / Persona Definition</div>
      <div class="dim-desc">Is there a clear role or persona set for the model?</div>
    </div>
    <div class="dim-item">
      <div class="dim-name">Output Format Instructions</div>
      <div class="dim-desc">Does the prompt specify the desired output format?</div>
    </div>
    <div class="dim-item">
      <div class="dim-name">Context &amp; Background</div>
      <div class="dim-desc">Is sufficient context provided for the task?</div>
    </div>
    <div class="dim-item">
      <div class="dim-name">Constraints &amp; Guardrails</div>
      <div class="dim-desc">Are limitations and boundaries clearly stated?</div>
    </div>
    <div class="dim-item">
      <div class="dim-name">Tone &amp; Style</div>
      <div class="dim-desc">Is the desired tone and style specified?</div>
    </div>
    <div class="dim-item">
      <div class="dim-name">Bias</div>
      <div class="dim-desc">Does the prompt avoid introducing unfair bias? Low score triggers a safety warning.</div>
    </div>
    <div class="dim-item">
      <div class="dim-name">Toxicity</div>
      <div class="dim-desc">Is the prompt free from harmful or offensive content? Low score triggers a safety warning.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Example Prompts
st.markdown("### Example Prompts")

with st.expander("❌ Weak prompt (before)"):
    st.code("Write something about climate change.", language=None)

with st.expander("✅ Strong prompt (after)"):
    st.code(
        "You are an environmental science communicator writing for a general audience. "
        "Write a 200-word explanation of the greenhouse effect and its relationship to "
        "climate change. Use simple language, avoid jargon, and end with one actionable "
        "step readers can take. Format as plain paragraphs.",
        language=None,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Setup
st.markdown("""
<div class="info-card">
  <h3>⚙️ Setup &amp; Configuration</h3>
  <p style="color:#475569;font-size:0.93rem;margin:0 0 0.9rem;">
    Before using the tool, configure your Databricks credentials:
  </p>
  <div class="setup-step">
    <div class="setup-icon">1️⃣</div>
    <div class="setup-text">Go to the <strong>Settings</strong> page in the sidebar</div>
  </div>
  <div class="setup-step">
    <div class="setup-icon">2️⃣</div>
    <div class="setup-text">Enter your <strong>Databricks Base URL</strong>, <strong>LLM Endpoint URL</strong>, and <strong>API Token</strong></div>
  </div>
  <div class="setup-step">
    <div class="setup-icon">3️⃣</div>
    <div class="setup-text">Click <strong>Save Settings</strong> — credentials are persisted on the server</div>
  </div>
  <div class="setup-step">
    <div class="setup-icon">✅</div>
    <div class="setup-text">Done! You only need to do this once.</div>
  </div>
</div>
""", unsafe_allow_html=True)
