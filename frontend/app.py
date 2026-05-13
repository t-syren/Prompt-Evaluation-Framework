import streamlit as st
from frontend.styles import base_css, nav_html, nav_close, inject_sidebar_killer

st.set_page_config(
    page_title="Prompt Evaluation Framework",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_sidebar_killer()
st.markdown(base_css(), unsafe_allow_html=True)
st.markdown(nav_html("home"), unsafe_allow_html=True)

st.markdown("""
<style>
/* ── HOME-ONLY: hero ── */
.hero {
  position: relative;
  min-height: 460px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  padding: 80px 40px 60px;
  overflow: hidden;
}
.hero-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black 0%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black 0%, transparent 100%);
  pointer-events: none;
}
.hero-glow-1 {
  position: absolute; width: 600px; height: 400px;
  background: radial-gradient(ellipse, rgba(255,54,33,0.18) 0%, transparent 65%);
  top: -80px; left: 50%; transform: translateX(-50%);
  animation: drift1 8s ease-in-out infinite alternate; pointer-events: none;
}
.hero-glow-2 {
  position: absolute; width: 400px; height: 300px;
  background: radial-gradient(ellipse, rgba(99,102,241,0.12) 0%, transparent 65%);
  bottom: 0; left: 5%;
  animation: drift2 10s ease-in-out infinite alternate; pointer-events: none;
}
.hero-glow-3 {
  position: absolute; width: 280px; height: 200px;
  background: radial-gradient(ellipse, rgba(20,184,166,0.1) 0%, transparent 65%);
  top: 40%; right: 5%;
  animation: drift3 7s ease-in-out infinite alternate; pointer-events: none;
}
@keyframes drift1 { from{transform:translateX(-55%) translateY(0)} to{transform:translateX(-45%) translateY(20px)} }
@keyframes drift2 { from{transform:translate(0,0)} to{transform:translate(30px,20px)} }
@keyframes drift3 { from{transform:translate(0,0)} to{transform:translate(-20px,15px)} }

.hero-badge {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 6px 14px;
  background: rgba(255,54,33,0.1); border: 1px solid rgba(255,54,33,0.25);
  border-radius: 20px; font-size: 11.5px; font-weight: 600; color: #ff8a75;
  letter-spacing: 0.04em; margin-bottom: 24px;
  animation: fadeUp 0.6s 0.05s both; position: relative; z-index: 1;
}
.hero-badge-dot {
  width: 5px; height: 5px; background: #FF3621; border-radius: 50%;
  box-shadow: 0 0 6px rgba(255,54,33,0.8);
}
.hero-title {
  font-size: 56px; font-weight: 900; letter-spacing: -0.04em; line-height: 1.05;
  margin-bottom: 20px; color: #f8fafc;
  animation: fadeUp 0.6s 0.1s both; position: relative; z-index: 1;
}
.hero-title-grad {
  background: linear-gradient(135deg, #FF3621 0%, #ff8a75 50%, #ffb3a7 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 17px; color: rgba(255,255,255,0.38); max-width: 520px;
  line-height: 1.65; margin-bottom: 36px;
  animation: fadeUp 0.6s 0.15s both; position: relative; z-index: 1;
}
.hero-actions {
  display: flex; align-items: center; gap: 12px;
  animation: fadeUp 0.6s 0.2s both; position: relative; z-index: 1;
}
.btn-hero-primary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #FF3621, #cc2c1a);
  border-radius: 10px; font-size: 14px; font-weight: 700; color: white;
  cursor: pointer; letter-spacing: -0.01em; text-decoration: none;
  box-shadow: 0 8px 32px rgba(255,54,33,0.4), 0 1px 0 rgba(255,255,255,0.12) inset;
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn-hero-primary:hover { transform: translateY(-2px); box-shadow: 0 14px 40px rgba(255,54,33,0.5); }
.btn-hero-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 22px;
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12);
  border-radius: 10px; font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.6);
  cursor: pointer; text-decoration: none;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}
.btn-hero-ghost:hover { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.85); border-color: rgba(255,255,255,0.2); }

/* ── STATS STRIP ── */
.stats-strip {
  display: flex; justify-content: center;
  border-top: 1px solid rgba(255,255,255,0.06);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  background: rgba(255,255,255,0.02);
  animation: fadeUp 0.6s 0.25s both;
}
.stat-item {
  flex: 1; max-width: 220px;
  padding: 24px 20px; text-align: center;
  border-right: 1px solid rgba(255,255,255,0.06);
}
.stat-item:last-child { border-right: none; }
.stat-num {
  font-size: 32px; font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, #FF3621, #ff8a75);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: -0.03em; line-height: 1; margin-bottom: 6px;
}
.stat-label { font-size: 12px; color: rgba(255,255,255,0.3); font-weight: 500; }

/* ── FEATURES ── */
.features-section { padding: 56px 0 32px; animation: fadeUp 0.6s 0.3s both; }
.section-eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: #FF3621; text-align: center; margin-bottom: 10px;
}
.section-title {
  font-size: 28px; font-weight: 800; color: #f1f5f9;
  text-align: center; letter-spacing: -0.03em; margin-bottom: 8px;
}
.section-sub { font-size: 14px; color: rgba(255,255,255,0.3); text-align: center; margin-bottom: 36px; }
.feature-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; max-width: 960px; margin: 0 auto; }
.feature-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 24px; cursor: pointer; position: relative; overflow: hidden;
  transition: background 0.2s, border-color 0.2s, transform 0.25s cubic-bezier(0.34,1.56,0.64,1);
}
.feature-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
  opacity: 0; transition: opacity 0.2s;
}
.feature-card:hover { background: rgba(255,255,255,0.055); border-color: rgba(255,255,255,0.14); transform: translateY(-4px); }
.feature-card:hover::before { opacity: 1; }
.feature-icon-wrap {
  width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center; margin-bottom: 16px;
}
.icon-red   { background: rgba(255,54,33,0.15);  box-shadow: 0 0 20px rgba(255,54,33,0.15); }
.icon-indigo{ background: rgba(99,102,241,0.15); box-shadow: 0 0 20px rgba(99,102,241,0.12); }
.icon-teal  { background: rgba(20,184,166,0.15); box-shadow: 0 0 20px rgba(20,184,166,0.10); }
.feature-title { font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px; letter-spacing: -0.01em; }
.feature-desc  { font-size: 13px; color: rgba(255,255,255,0.35); line-height: 1.6; }
.feature-cta {
  display: inline-flex; align-items: center; gap: 5px;
  margin-top: 16px; font-size: 12.5px; font-weight: 600;
  color: rgba(255,255,255,0.35); transition: color 0.2s; text-decoration: none;
}
.feature-card:hover .feature-cta { color: rgba(255,255,255,0.7); }

/* ── HOW IT WORKS ── */
.steps-section { padding: 20px 0 64px; max-width: 960px; margin: 0 auto; animation: fadeUp 0.6s 0.35s both; }
.steps-row { display: flex; gap: 0; position: relative; }
.steps-row::before {
  content: ''; position: absolute; top: 22px; left: 22px; right: 22px; height: 1px;
  background: linear-gradient(90deg, rgba(255,54,33,0.4), rgba(255,54,33,0.15), rgba(255,54,33,0.4));
}
.step { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 16px; position: relative; }
.step-num {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, #FF3621, #cc2c1a);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 800; font-family: 'JetBrains Mono', monospace;
  color: white; margin-bottom: 16px;
  box-shadow: 0 0 24px rgba(255,54,33,0.4); position: relative; z-index: 1;
}
.step-title { font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.8); margin-bottom: 6px; }
.step-desc  { font-size: 12px; color: rgba(255,255,255,0.3); line-height: 1.55; }
</style>

<!-- HERO -->
<div class="hero">
  <div class="hero-grid"></div>
  <div class="hero-glow-1"></div>
  <div class="hero-glow-2"></div>
  <div class="hero-glow-3"></div>
  <div class="hero-badge">
    <div class="hero-badge-dot"></div>
    Powered by DeepEval &amp; Databricks Claude
  </div>
  <h1 class="hero-title">Smarter prompts,<br><span class="hero-title-grad">scored instantly.</span></h1>
  <p class="hero-sub">Paste any LLM prompt. Get scored across 8 quality dimensions — clarity, role, format, context, constraints, tone, bias, toxicity — with AI-powered fixes in seconds.</p>
  <div class="hero-actions">
    <a class="btn-hero-primary" href="/Evaluate_Fix" target="_self">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M3.5 8h4l2.5-5 2 10 2.5-5" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Evaluate a Prompt
    </a>
    <a class="btn-hero-ghost" href="/Get_Started" target="_self">
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
        <circle cx="7.5" cy="7.5" r="6" stroke="currentColor" stroke-width="1.5"/>
        <path d="M7.5 5v3l2 1.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      How it works
    </a>
  </div>
</div>

<!-- STATS -->
<div class="stats-strip">
  <div class="stat-item"><div class="stat-num">8</div><div class="stat-label">Quality dimensions</div></div>
  <div class="stat-item"><div class="stat-num">1–10</div><div class="stat-label">Score scale</div></div>
  <div class="stat-item"><div class="stat-num">3</div><div class="stat-label">Fix variants</div></div>
  <div class="stat-item"><div class="stat-num">360°</div><div class="stat-label">Safety coverage</div></div>
</div>

<!-- FEATURES -->
<div class="features-section">
  <div class="section-eyebrow">What PEF does</div>
  <div class="section-title">Everything your prompt needs</div>
  <div class="section-sub">From first evaluation to production-ready — in one place.</div>
  <div class="feature-grid">
    <div class="feature-card">
      <div class="feature-icon-wrap icon-red">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <path d="M5 11h4l3-6 2 12 3-6" stroke="#FF3621" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="feature-title">Deep Evaluation</div>
      <div class="feature-desc">G-Eval across 6 quality dimensions plus Bias &amp; Toxicity safety metrics. Chain-of-thought reasoning explains every score.</div>
      <a class="feature-cta" href="/Evaluate_Fix" target="_self">Start evaluating <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    </div>
    <div class="feature-card">
      <div class="feature-icon-wrap icon-indigo">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <path d="M11 4v4M11 14v4M4 11h4M14 11h4" stroke="#818cf8" stroke-width="1.7" stroke-linecap="round"/>
          <circle cx="11" cy="11" r="3" stroke="#818cf8" stroke-width="1.7"/>
        </svg>
      </div>
      <div class="feature-title">Auto-Fix &amp; Refine</div>
      <div class="feature-desc">Get a single best fix or 3 variants to compare. Regression guard ensures fixes never lower a passing dimension.</div>
      <a class="feature-cta" href="/Evaluate_Fix" target="_self">Fix a prompt <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    </div>
    <div class="feature-card">
      <div class="feature-icon-wrap icon-teal">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <path d="M11 4L18 8v6L11 18 4 14V8L11 4z" stroke="#2dd4bf" stroke-width="1.7" stroke-linejoin="round"/>
          <path d="M11 9v3l2 1" stroke="#2dd4bf" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="feature-title">Stress &amp; Hallucination</div>
      <div class="feature-desc">Probe adversarial robustness with jailbreak attacks. Detect hallucination risk before your prompt hits production.</div>
      <a class="feature-cta" href="/Evaluate_Fix" target="_self">Run a test <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    </div>
  </div>
</div>

<!-- HOW IT WORKS -->
<div class="steps-section">
  <div class="section-eyebrow" style="margin-bottom:10px;">How it works</div>
  <div class="section-title" style="margin-bottom:40px;">From paste to production-ready</div>
  <div class="steps-row">
    <div class="step"><div class="step-num">1</div><div class="step-title">Paste your prompt</div><div class="step-desc">Any LLM prompt — system prompt, user message, or full template.</div></div>
    <div class="step"><div class="step-num">2</div><div class="step-title">Evaluate</div><div class="step-desc">DeepEval scores all 8 dimensions with full chain-of-thought reasoning.</div></div>
    <div class="step"><div class="step-num">3</div><div class="step-title">Fix &amp; Compare</div><div class="step-desc">Auto-generate an improved prompt. Compare before/after scores side by side.</div></div>
    <div class="step"><div class="step-num">4</div><div class="step-title">Stress test</div><div class="step-desc">Run adversarial attacks and hallucination checks. Ship with confidence.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(nav_close(), unsafe_allow_html=True)
