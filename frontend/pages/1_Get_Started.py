import streamlit as st
from frontend.styles import base_css, nav_html, nav_close, inject_sidebar_killer

st.set_page_config(page_title="Get Started — PEF", page_icon=None, layout="wide",
                   initial_sidebar_state="collapsed")

inject_sidebar_killer()
st.markdown(base_css(), unsafe_allow_html=True)
st.markdown(nav_html("get_started"), unsafe_allow_html=True)

st.markdown("""
<style>
.page-header { margin-bottom: 28px; animation: fadeUp 0.5s 0.05s both; }
.page-title  { font-size: 24px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.025em; margin-bottom: 6px; }
.page-sub    { font-size: 14px; color: rgba(255,255,255,0.35); }

/* step rows */
.step-row    { display: flex; align-items: flex-start; gap: 14px; margin-bottom: 14px; }
.step-badge  {
  width: 28px; height: 28px; flex-shrink: 0;
  background: linear-gradient(135deg, #FF3621, #cc2c1a);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800; font-family: 'JetBrains Mono', monospace;
  color: white; box-shadow: 0 0 12px rgba(255,54,33,0.35);
}
.step-text   { font-size: 14px; color: rgba(255,255,255,0.6); line-height: 1.6; padding-top: 4px; }
.step-text strong { color: rgba(255,255,255,0.85); }

/* dimension grid */
.dim-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 4px; }
.dim-card {
  background: rgba(255,54,33,0.07); border: 1px solid rgba(255,54,33,0.18);
  border-radius: 10px; padding: 12px 14px;
}
.dim-name { font-weight: 700; color: #ff8a75; font-size: 13px; margin-bottom: 4px; }
.dim-desc { color: rgba(255,255,255,0.4); font-size: 12px; line-height: 1.4; }

/* example prompts */
.example-label {
  font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
  margin-bottom: 8px;
}
.example-label.bad  { color: #f87171; }
.example-label.good { color: #4ade80; }
.example-code {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px; padding: 14px 16px;
  font-family: 'JetBrains Mono', monospace; font-size: 12.5px;
  color: rgba(255,255,255,0.65); line-height: 1.6; white-space: pre-wrap;
}

/* setup rows */
.setup-row { display: flex; align-items: flex-start; gap: 14px; margin-bottom: 12px; }
.setup-icon-wrap {
  width: 32px; height: 32px; flex-shrink: 0; border-radius: 8px;
  background: rgba(255,255,255,0.06);
  display: flex; align-items: center; justify-content: center;
}
.setup-text { font-size: 13.5px; color: rgba(255,255,255,0.55); line-height: 1.6; padding-top: 5px; }
.setup-text strong { color: rgba(255,255,255,0.85); }
</style>

<div class="page-header anim-1">
  <div class="page-title">Get Started</div>
  <div class="page-sub">Everything you need to know to get the most from PEF.</div>
</div>

<!-- What is PEF -->
<div class="glass-card anim-2">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <circle cx="7" cy="7" r="5" stroke="rgba(255,255,255,0.4)" stroke-width="1.4"/>
      <path d="M7 6v4M7 4.5v.5" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    <span class="card-label">What is PEF?</span>
  </div>
  <div class="glass-card-body">
    <p style="font-size:14px;color:rgba(255,255,255,0.6);line-height:1.7;margin:0;">
      The <strong style="color:rgba(255,255,255,0.85);">Prompt Evaluation Framework</strong> is an AI-powered tool that analyzes any LLM prompt and tells you exactly what's working, what isn't, and how to improve it — instantly. It scores your prompt across 8 quality dimensions powered by DeepEval and can automatically rewrite it for you. Safety metrics (Bias &amp; Toxicity) are checked automatically on every evaluation.
    </p>
  </div>
</div>

<!-- How It Works -->
<div class="glass-card anim-3">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <path d="M3 7h3l2-4 2 8 2-4" stroke="rgba(255,255,255,0.4)" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span class="card-label">How It Works</span>
  </div>
  <div class="glass-card-body">
    <div class="step-row"><div class="step-badge">1</div><div class="step-text"><strong>Paste your prompt</strong> on the Evaluate &amp; Fix page.</div></div>
    <div class="step-row"><div class="step-badge">2</div><div class="step-text"><strong>Click Analyze</strong> — DeepEval scores your prompt across 8 quality dimensions with chain-of-thought reasoning.</div></div>
    <div class="step-row"><div class="step-badge">3</div><div class="step-text"><strong>Review the scorecard</strong> — see AI analysis, specific issues, and improvement suggestions per dimension.</div></div>
    <div class="step-row"><div class="step-badge">4</div><div class="step-text"><strong>Click Fix Prompt</strong> — generate an improved version; the fixer validates regressions automatically.</div></div>
    <div class="step-row"><div class="step-badge">5</div><div class="step-text"><strong>Run stress test or hallucination check</strong> — probe adversarial robustness and factual accuracy.</div></div>
    <div class="step-row" style="margin-bottom:0"><div class="step-badge">6</div><div class="step-text"><strong>Download or copy</strong> your improved prompt and evaluation report.</div></div>
  </div>
</div>

<!-- Dimensions -->
<div class="glass-card anim-4">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <rect x="2" y="2" width="4" height="4" rx="1" stroke="rgba(255,255,255,0.4)" stroke-width="1.3"/>
      <rect x="8" y="2" width="4" height="4" rx="1" stroke="rgba(255,255,255,0.4)" stroke-width="1.3"/>
      <rect x="2" y="8" width="4" height="4" rx="1" stroke="rgba(255,255,255,0.4)" stroke-width="1.3"/>
      <rect x="8" y="8" width="4" height="4" rx="1" stroke="rgba(255,255,255,0.4)" stroke-width="1.3"/>
    </svg>
    <span class="card-label">Evaluation Dimensions</span>
    <span style="margin-left:auto;font-size:11px;color:rgba(255,255,255,0.2);">8 total · scored 1–10</span>
  </div>
  <div class="glass-card-body">
    <div class="dim-grid">
      <div class="dim-card"><div class="dim-name">Clarity &amp; Specificity</div><div class="dim-desc">Is the prompt unambiguous and precise?</div></div>
      <div class="dim-card"><div class="dim-name">Role / Persona</div><div class="dim-desc">Is there a clear role or persona set for the model?</div></div>
      <div class="dim-card"><div class="dim-name">Output Format</div><div class="dim-desc">Does the prompt specify the desired output format?</div></div>
      <div class="dim-card"><div class="dim-name">Context &amp; Background</div><div class="dim-desc">Is sufficient context provided for the task?</div></div>
      <div class="dim-card"><div class="dim-name">Constraints &amp; Guardrails</div><div class="dim-desc">Are limitations and boundaries clearly stated?</div></div>
      <div class="dim-card"><div class="dim-name">Tone &amp; Style</div><div class="dim-desc">Is the desired tone and style specified?</div></div>
      <div class="dim-card"><div class="dim-name">Bias</div><div class="dim-desc">Does the prompt avoid introducing unfair bias?</div></div>
      <div class="dim-card"><div class="dim-name">Toxicity</div><div class="dim-desc">Is the prompt free from harmful or offensive content?</div></div>
    </div>
  </div>
</div>

<!-- Example Prompts -->
<div class="glass-card anim-5">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <rect x="2" y="2" width="10" height="10" rx="2" stroke="rgba(255,255,255,0.4)" stroke-width="1.3"/>
      <path d="M4.5 5h5M4.5 7.5h3" stroke="rgba(255,255,255,0.4)" stroke-width="1.3" stroke-linecap="round"/>
    </svg>
    <span class="card-label">Example Prompts</span>
  </div>
  <div class="glass-card-body">
    <div style="margin-bottom:16px;">
      <div class="example-label bad">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none" style="vertical-align:middle;margin-right:4px;">
          <circle cx="5" cy="5" r="4" stroke="#f87171" stroke-width="1.3"/>
          <path d="M3.5 3.5l3 3M6.5 3.5l-3 3" stroke="#f87171" stroke-width="1.3" stroke-linecap="round"/>
        </svg>
        Weak prompt
      </div>
      <div class="example-code">Write something about climate change.</div>
    </div>
    <div>
      <div class="example-label good">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none" style="vertical-align:middle;margin-right:4px;">
          <circle cx="5" cy="5" r="4" stroke="#4ade80" stroke-width="1.3"/>
          <path d="M2.5 5l2 2 3-3" stroke="#4ade80" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Strong prompt
      </div>
      <div class="example-code">You are an environmental science communicator writing for a general audience. Write a 200-word explanation of the greenhouse effect and its relationship to climate change. Use simple language, avoid jargon, and end with one actionable step readers can take. Format as plain paragraphs.</div>
    </div>
  </div>
</div>

<!-- Setup -->
<div class="glass-card" style="animation:fadeUp 0.5s 0.3s both;">
  <div class="glass-card-header">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <circle cx="7" cy="7" r="2" stroke="rgba(255,255,255,0.4)" stroke-width="1.4"/>
      <path d="M7 1.5v1.7M7 10.8v1.7M1.5 7h1.7M10.8 7h1.7M3.4 3.4l1.2 1.2M9.4 9.4l1.2 1.2M10.6 3.4L9.4 4.6M4.6 9.4L3.4 10.6" stroke="rgba(255,255,255,0.4)" stroke-width="1.3" stroke-linecap="round"/>
    </svg>
    <span class="card-label">Setup &amp; Configuration</span>
  </div>
  <div class="glass-card-body">
    <p style="font-size:13px;color:rgba(255,255,255,0.4);margin:0 0 16px;">Before using the tool, configure your Databricks credentials:</p>
    <div class="setup-row">
      <div class="setup-icon-wrap">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L7 2l5 5M3.5 5.5V11.5h7V5.5" stroke="rgba(255,255,255,0.5)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="setup-text">Go to the <strong>Settings</strong> page in the top nav.</div>
    </div>
    <div class="setup-row">
      <div class="setup-icon-wrap">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><rect x="3" y="5" width="8" height="6" rx="1.5" stroke="rgba(255,255,255,0.5)" stroke-width="1.3"/><path d="M5 5V4a2 2 0 014 0v1" stroke="rgba(255,255,255,0.5)" stroke-width="1.3" stroke-linecap="round"/></svg>
      </div>
      <div class="setup-text">Enter your <strong>Databricks Base URL</strong>, <strong>LLM Endpoint URL</strong>, and <strong>API Token</strong>.</div>
    </div>
    <div class="setup-row">
      <div class="setup-icon-wrap">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7h10M7 2v10" stroke="rgba(255,255,255,0.5)" stroke-width="1.3" stroke-linecap="round"/></svg>
      </div>
      <div class="setup-text">Click <strong>Save Settings</strong> — credentials persist on the server.</div>
    </div>
    <div class="setup-row" style="margin-bottom:0;">
      <div class="setup-icon-wrap">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7l3 3 6-6" stroke="#4ade80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="setup-text">Done — you only need to do this once.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(nav_close(), unsafe_allow_html=True)
