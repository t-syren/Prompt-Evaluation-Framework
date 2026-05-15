# PEF UI Redesign — Glass Premium Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace sidebar navigation and default Streamlit styling with a Glass Premium dark-theme UI — sticky top nav, glassmorphism cards, animated radial glows, SVG icons, gradient score numbers — across all 4 pages, zero backend changes.

**Architecture:** A new `frontend/styles.py` exports `base_css()` (complete CSS string) and `nav_html(active)` (top nav HTML with active link highlighted, opens `.page-bg` div). Every page imports these two functions, inserts them via `st.markdown(..., unsafe_allow_html=True)`, and closes with `st.markdown("</div>", unsafe_allow_html=True)`. All Python logic in `2_Evaluate_Fix.py` (API calls, threading, session state, `build_scorecard_report`) is preserved unchanged.

**Tech Stack:** Streamlit, Python 3.8+, Inter + JetBrains Mono (Google Fonts), inline SVG, custom HTML/CSS — no new pip packages.

---

## File Map

| File | Action | Scope |
|---|---|---|
| `frontend/styles.py` | **Create** | Shared CSS + nav HTML |
| `frontend/app.py` | **Full rewrite** | Home — hero, stats, features, how-it-works |
| `frontend/pages/1_Get_Started.py` | **Full rewrite** | Docs — glass cards, dim grid, steps |
| `frontend/pages/2_Evaluate_Fix.py` | **Partial rewrite** | CSS block, 3 render functions, HTML wrappers; all logic preserved |
| `frontend/pages/3_Settings.py` | **Full rewrite** | Settings forms in glass cards |
| `.gitignore` | **Modify** | Add `.superpowers/` |

---

### Task 1: Create shared styles module

**Files:**
- Create: `frontend/styles.py`

- [ ] **Step 1: Verify baseline — 64 tests pass**

```bash
./venv/bin/pytest tests/ -v --tb=short 2>&1 | tail -5
```
Expected: `64 passed`

- [ ] **Step 2: Create `frontend/styles.py`**

```python
# frontend/styles.py
_FONTS = (
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900"
    "&family=JetBrains+Mono:wght@400;500;600&display=swap"
)


def base_css() -> str:
    return f"""
<style>
@import url('{_FONTS}');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, .stApp {{
  font-family: 'Inter', sans-serif !important;
  background: #09090e !important;
  color: #e2e8f0 !important;
}}

/* ── Sidebar: hide completely ── */
[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}

/* ── Remove Streamlit default padding ── */
.main .block-container {{
  padding-top: 0 !important;
  padding-left: 28px !important;
  padding-right: 28px !important;
  max-width: 100% !important;
}}
#MainMenu, footer, header {{ visibility: hidden !important; }}

/* ── TOP NAV ── */
.topnav {{
  position: sticky; top: 0; z-index: 999;
  height: 52px;
  background: rgba(9,9,14,0.82);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.07);
  display: flex; align-items: center;
  padding: 0 28px;
  margin: 0 -28px;
}}
.nav-logo {{
  display: flex; align-items: center; gap: 9px;
  margin-right: 32px; text-decoration: none;
}}
.logo-mark {{
  width: 28px; height: 28px;
  background: linear-gradient(135deg, #FF3621, #ff6b52);
  border-radius: 7px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 16px rgba(255,54,33,0.4); flex-shrink: 0;
}}
.logo-wordmark {{ font-size: 14px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; }}
.nav-divider {{ width: 1px; height: 18px; background: rgba(255,255,255,0.1); margin-right: 24px; }}
.nav-links {{ display: flex; align-items: center; gap: 2px; flex: 1; }}
.nav-link {{
  display: flex; align-items: center; gap: 6px;
  padding: 6px 12px; border-radius: 8px;
  font-size: 13px; font-weight: 500;
  color: rgba(255,255,255,0.4); text-decoration: none;
  transition: background .15s, color .15s;
}}
.nav-link:hover {{ background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.75); }}
.nav-link.active {{ background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.9); font-weight: 600; }}
.nav-link svg {{ opacity: 0.6; flex-shrink: 0; vertical-align: middle; }}
.nav-link.active svg {{ opacity: 1; }}
.nav-status {{
  display: flex; align-items: center; gap: 6px;
  padding: 5px 12px;
  background: rgba(22,163,74,0.12); border: 1px solid rgba(22,163,74,0.2);
  border-radius: 20px; font-size: 11.5px; font-weight: 600; color: #4ade80;
}}
.status-dot {{
  width: 6px; height: 6px; background: #4ade80; border-radius: 50%;
  box-shadow: 0 0 8px rgba(74,222,128,0.6);
  animation: pulseDot 2s ease-in-out infinite;
}}

/* ── PAGE BACKGROUND ── */
.page-bg {{
  min-height: calc(100vh - 52px);
  background:
    radial-gradient(ellipse 60% 40% at 15% 0%, rgba(255,54,33,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 85% 20%, rgba(99,102,241,0.10) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 60% 90%, rgba(6,182,212,0.07) 0%, transparent 60%),
    #09090e;
  padding: 32px 0 80px;
}}

/* ── GLASS CARD ── */
.glass-card {{
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 16px; overflow: hidden; margin-bottom: 20px;
}}
.glass-card-header {{
  padding: 14px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center; gap: 10px;
}}
.card-label {{
  font-size: 11px; font-weight: 700;
  letter-spacing: 0.09em; text-transform: uppercase;
  color: rgba(255,255,255,0.35);
}}
.card-label-accent {{
  font-size: 11px; font-weight: 700;
  letter-spacing: 0.06em; text-transform: uppercase; color: #FF3621;
}}
.glass-card-body {{ padding: 20px; }}

/* ── BUTTONS ── */
.stButton > button {{
  font-family: 'Inter', sans-serif !important;
  border-radius: 9px !important; font-weight: 600 !important;
  font-size: 13px !important; letter-spacing: 0.01em !important;
  transition: transform 0.15s, box-shadow 0.15s !important;
}}
.stButton > button[kind="primary"] {{
  background: linear-gradient(135deg, #FF3621, #cc2c1a) !important;
  border: none !important; color: white !important;
  -webkit-text-fill-color: white !important;
  box-shadow: 0 4px 20px rgba(255,54,33,0.35) !important;
}}
.stButton > button[kind="primary"]:hover {{
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 28px rgba(255,54,33,0.48) !important;
}}
.stButton > button:not([kind="primary"]) {{
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: rgba(255,255,255,0.6) !important;
}}
.stButton > button:not([kind="primary"]) p,
.stButton > button:not([kind="primary"]) * {{
  color: rgba(255,255,255,0.6) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.6) !important;
}}
.stButton > button:not([kind="primary"]):hover {{
  background: rgba(255,255,255,0.08) !important;
  color: rgba(255,255,255,0.85) !important;
}}
.stDownloadButton > button, [data-testid="stDownloadButton"] button {{
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: rgba(255,255,255,0.6) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.6) !important;
  border-radius: 9px !important; font-weight: 600 !important;
}}
.stDownloadButton > button p, [data-testid="stDownloadButton"] button p {{
  color: rgba(255,255,255,0.6) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.6) !important;
}}

/* ── TEXT INPUTS ── */
.stTextArea textarea {{
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: rgba(255,255,255,0.85) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.85) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13.5px !important; line-height: 1.65 !important;
  caret-color: #FF3621 !important;
}}
.stTextArea textarea:focus {{
  border-color: rgba(255,54,33,0.4) !important;
  box-shadow: 0 0 0 3px rgba(255,54,33,0.1) !important;
}}
.stTextArea textarea::placeholder {{
  color: rgba(255,255,255,0.2) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.2) !important;
}}
.stTextInput > div > div > input {{
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 8px !important;
  color: rgba(255,255,255,0.85) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.85) !important;
}}
.stTextInput > div > div > input:focus {{
  border-color: rgba(255,54,33,0.4) !important;
  box-shadow: 0 0 0 3px rgba(255,54,33,0.1) !important;
}}
.stTextArea label, .stTextInput label, [data-testid="stWidgetLabel"] p {{
  color: rgba(255,255,255,0.45) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.45) !important;
}}

/* ── SELECT / TOGGLE / RADIO ── */
[data-baseweb="select"] > div {{
  background: rgba(255,255,255,0.04) !important;
  border-color: rgba(255,255,255,0.1) !important;
  border-radius: 8px !important;
  color: rgba(255,255,255,0.8) !important;
}}
[data-baseweb="select"] * {{ color: rgba(255,255,255,0.8) !important; }}
.stRadio > label {{ color: rgba(255,255,255,0.5) !important; }}
.stRadio [data-testid="stMarkdownContainer"] p {{ color: rgba(255,255,255,0.75) !important; }}

/* ── TABS ── */
.stTabs [data-baseweb="tab"] {{ color: rgba(255,255,255,0.45) !important; font-weight: 500 !important; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color: #FF3621 !important; }}
.stTabs [aria-selected="true"] {{ color: rgba(255,255,255,0.9) !important; }}
.stTabs [data-baseweb="tab-list"] {{
  background: rgba(255,255,255,0.02) !important;
  border-bottom: 1px solid rgba(255,255,255,0.07) !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 16px !important; }}

/* ── EXPANDERS ── */
details {{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 10px !important; margin-bottom: 6px !important;
}}
details * {{ color: rgba(255,255,255,0.7) !important; }}
summary {{
  font-weight: 500 !important; padding: 0.6rem 1rem !important;
  color: rgba(255,255,255,0.65) !important;
}}

/* ── STATUS / ALERTS / SPINNER ── */
.stProgress > div > div > div > div {{
  background: linear-gradient(90deg, #FF3621, #ff6b52) !important;
  border-radius: 4px !important;
}}
.stAlert {{ border-radius: 10px !important; }}
.stSpinner > div {{ border-top-color: #FF3621 !important; }}
hr {{ border-color: rgba(255,255,255,0.08) !important; }}

/* ── TYPOGRAPHY ── */
p, li {{ color: rgba(255,255,255,0.65); }}
.stMarkdown p, .stMarkdown li {{ color: rgba(255,255,255,0.65) !important; }}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {{ color: rgba(255,255,255,0.65) !important; }}
h1 {{ color: #f1f5f9 !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }}
h2, h3 {{ color: rgba(255,255,255,0.85) !important; }}
code {{
  background: rgba(255,255,255,0.07) !important;
  color: #ff8a75 !important; border-radius: 4px !important;
  padding: 2px 6px !important; font-family: 'JetBrains Mono', monospace !important;
}}

/* ── ANIMATIONS ── */
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(16px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulseDot {{
  0%,100% {{ opacity: 1; transform: scale(1); }}
  50%     {{ opacity: 0.6; transform: scale(0.85); }}
}}

.anim-1 {{ animation: fadeUp 0.5s 0.05s both; }}
.anim-2 {{ animation: fadeUp 0.5s 0.10s both; }}
.anim-3 {{ animation: fadeUp 0.5s 0.15s both; }}
.anim-4 {{ animation: fadeUp 0.5s 0.20s both; }}
.anim-5 {{ animation: fadeUp 0.5s 0.25s both; }}
</style>
"""


def nav_html(active: str) -> str:
    """
    Render the sticky top nav + open .page-bg wrapper.
    active: 'home' | 'get_started' | 'evaluate' | 'settings'
    Call nav_close() at the bottom of every page.
    """
    def _cls(key: str) -> str:
        return "nav-link active" if active == key else "nav-link"

    return f"""
<nav class="topnav">
  <a class="nav-logo" href="/">
    <div class="logo-mark">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M7 2L12 5V9L7 12L2 9V5L7 2Z" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
        <circle cx="7" cy="7" r="1.5" fill="white"/>
      </svg>
    </div>
    <span class="logo-wordmark">PEF</span>
  </a>
  <div class="nav-divider"></div>
  <div class="nav-links">
    <a class="{_cls('home')}" href="/">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M2 7L7 2l5 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M3.5 5.5V11a.5.5 0 00.5.5h2.5V8.5h2V11.5H11a.5.5 0 00.5-.5V5.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Home
    </a>
    <a class="{_cls('get_started')}" href="/Get_Started">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.4"/>
        <path d="M7 4.5v3l1.5 1.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
      </svg>
      Get Started
    </a>
    <a class="{_cls('evaluate')}" href="/Evaluate_Fix">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M3 7h3l2-4 2 8 2-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Evaluate &amp; Fix
    </a>
    <a class="{_cls('settings')}" href="/Settings">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <circle cx="7" cy="7" r="2" stroke="currentColor" stroke-width="1.4"/>
        <path d="M7 1.5v1.7M7 10.8v1.7M1.5 7h1.7M10.8 7h1.7M3.4 3.4l1.2 1.2M9.4 9.4l1.2 1.2M10.6 3.4L9.4 4.6M4.6 9.4L3.4 10.6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
      </svg>
      Settings
    </a>
  </div>
  <div class="nav-status">
    <div class="status-dot"></div>
    Connected
  </div>
</nav>
<div class="page-bg">
"""


def nav_close() -> str:
    """Close the .page-bg div opened by nav_html."""
    return "</div>"
```

- [ ] **Step 3: Commit**

```bash
git add frontend/styles.py
git commit -m "feat(ui): add shared Glass Premium CSS + nav module"
```

---

### Task 2: Rewrite Home page

**Files:**
- Modify: `frontend/app.py`

- [ ] **Step 1: Replace `frontend/app.py` entirely**

```python
import streamlit as st
from frontend.styles import base_css, nav_html, nav_close

st.set_page_config(
    page_title="Prompt Evaluation Framework",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
  cursor: pointer; letter-spacing: -0.01em;
  box-shadow: 0 8px 32px rgba(255,54,33,0.4), 0 1px 0 rgba(255,255,255,0.12) inset;
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn-hero-primary:hover { transform: translateY(-2px); box-shadow: 0 14px 40px rgba(255,54,33,0.5); }
.btn-hero-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 22px;
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12);
  border-radius: 10px; font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.6);
  cursor: pointer; transition: background 0.2s, color 0.2s, border-color 0.2s;
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
    <a class="btn-hero-primary" href="/Evaluate_Fix">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M3.5 8h4l2.5-5 2 10 2.5-5" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Evaluate a Prompt
    </a>
    <a class="btn-hero-ghost" href="/Get_Started">
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
      <a class="feature-cta" href="/Evaluate_Fix">Start evaluating <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
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
      <a class="feature-cta" href="/Evaluate_Fix">Fix a prompt <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
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
      <a class="feature-cta" href="/Evaluate_Fix">Run a test <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
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
```

- [ ] **Step 2: Visual check — run the app and open Home**

```bash
./venv/bin/streamlit run frontend/app.py --server.port 8501 &
# Open http://localhost:8501 — verify: dark background, top nav, hero with glows, stats strip, 3 feature cards, 4-step row
# Kill with: kill %1
```

- [ ] **Step 3: Commit**

```bash
git add frontend/app.py
git commit -m "feat(ui): redesign Home page — Glass Premium hero, stats, features"
```

---

### Task 3: Rewrite Get Started page

**Files:**
- Modify: `frontend/pages/1_Get_Started.py`

- [ ] **Step 1: Replace `frontend/pages/1_Get_Started.py` entirely**

```python
import streamlit as st
from frontend.styles import base_css, nav_html, nav_close

st.set_page_config(page_title="Get Started — PEF", page_icon="📖", layout="wide",
                   initial_sidebar_state="collapsed")

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
```

- [ ] **Step 2: Visual check**

```bash
# With the app already running, navigate to /Get_Started
# Verify: top nav active on "Get Started", dark theme, glass cards, dim grid 2-col, SVG step badges
```

- [ ] **Step 3: Commit**

```bash
git add frontend/pages/1_Get_Started.py
git commit -m "feat(ui): redesign Get Started page — glass cards, dim grid, SVG steps"
```

---

### Task 4: Rewrite Evaluate & Fix page

**Files:**
- Modify: `frontend/pages/2_Evaluate_Fix.py`

This file is 1148 lines. The Python logic (imports, API helpers, `_run_pipeline_bg`, `score_color`, `score_emoji`, `build_scorecard_report`, session state) is **preserved exactly**. Only the CSS block, render functions, and HTML wrapper fragments are replaced.

- [ ] **Step 1: Replace `set_page_config` and CSS block (lines 1–157)**

Replace everything from line 1 through the closing `""", unsafe_allow_html=True)` of the style block with:

```python
import os
import time
import threading
from typing import Optional, List, Tuple
import httpx
import streamlit as st
from datetime import datetime, timezone
from frontend.styles import base_css, nav_html, nav_close

st.set_page_config(page_title="Evaluate & Fix — PEF", page_icon="🔍", layout="wide",
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
```

- [ ] **Step 2: Remove the scroll-to-top `st_components.html` block**

Delete the entire block starting with `import streamlit.components.v1 as st_components` (import at top) and the `st_components.html("""...""", height=0, scrolling=False)` call (~lines 530–562). Also remove `import streamlit.components.v1 as st_components` from the imports at the top.

- [ ] **Step 3: Replace `render_score_overview` function**

Find and replace the entire `render_score_overview` function:

```python
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
    tc_avg, _, _ = score_color(round(avg))
    avg_cls = "sg" if avg >= 7 else ("sw" if avg >= 4 else "sb")
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
```

- [ ] **Step 4: Replace `render_scorecard_details` function**

```python
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
```

- [ ] **Step 5: Replace `render_comparison` function**

```python
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
```

- [ ] **Step 6: Replace prompt input wrapper HTML**

Find the section starting with `st.markdown("""\n<div style="background:white;...` (around line 636) and replace just that HTML wrapper block:

```python
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
```

And the closing `st.markdown("</div>", unsafe_allow_html=True)` after the text area remains as-is.

- [ ] **Step 7: Replace scorecard section header HTML**

Find and replace the scorecard header block (the `st.markdown` with "📊 Evaluation Scorecard"):

```python
# (no header needed — render_score_overview now renders the full glass card with header)
```

Delete those lines entirely — the overall score is now part of `render_score_overview`.

- [ ] **Step 8: Replace stress test result HTML**

Find the `if st.session_state.stress_test_result:` block HTML wrapper and replace:

```python
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
```

- [ ] **Step 9: Replace hallucination result HTML**

Find the `if st.session_state.hallucination_result:` block and replace:

```python
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
```

- [ ] **Step 10: Replace Fix section header and wrap**

Find `st.markdown("<hr>", unsafe_allow_html=True)` followed by the "🔧 Fix Your Prompt" header block, and replace:

```python
st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:24px 0;'>", unsafe_allow_html=True)
st.markdown('<div class="fix-section-title">Fix Your Prompt</div>', unsafe_allow_html=True)
```

Find the "✨ Improved Prompt" header block and replace:

```python
st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:24px 0;'>", unsafe_allow_html=True)
st.markdown('<div class="fix-section-title">Improved Prompt</div>', unsafe_allow_html=True)
```

- [ ] **Step 11: Add `nav_close()` at the very end of the file**

```python
st.markdown(nav_close(), unsafe_allow_html=True)
```

- [ ] **Step 12: Visual check**

```bash
# Navigate to /Evaluate_Fix — enter a prompt and click Analyze
# Verify: dark theme, glass prompt card, 4×2 score grid with gradient bars, detail rows with badges,
#         3 action cards, stress/hallucination tiles styled correctly
```

- [ ] **Step 13: Confirm existing tests still pass**

```bash
./venv/bin/pytest tests/ -v --tb=short 2>&1 | tail -5
```
Expected: `64 passed`

- [ ] **Step 14: Commit**

```bash
git add frontend/pages/2_Evaluate_Fix.py
git commit -m "feat(ui): redesign Evaluate & Fix — glass scorecard, score grid, action cards"
```

---

### Task 5: Rewrite Settings page

**Files:**
- Modify: `frontend/pages/3_Settings.py`

- [ ] **Step 1: Replace `frontend/pages/3_Settings.py` entirely**

```python
import os
from typing import Optional
import httpx
import streamlit as st
from frontend.styles import base_css, nav_html, nav_close

st.set_page_config(page_title="Settings — PEF", page_icon="⚙️", layout="wide",
                   initial_sidebar_state="collapsed")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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
```

- [ ] **Step 2: Visual check**

```bash
# Navigate to /Settings
# Verify: dark theme, glass cards for connection form and defaults, token badge, toggle styles
```

- [ ] **Step 3: Commit**

```bash
git add frontend/pages/3_Settings.py
git commit -m "feat(ui): redesign Settings page — glass cards, dark inputs, token badge"
```

---

### Task 6: Housekeeping and final verification

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add `.superpowers/` to `.gitignore`**

```bash
echo '.superpowers/' >> .gitignore
git add .gitignore
```

- [ ] **Step 2: Final test run — confirm 64 tests still pass**

```bash
./venv/bin/pytest tests/ -v --tb=short 2>&1 | tail -10
```
Expected: `64 passed`

- [ ] **Step 3: Full visual QA — run the complete app**

```bash
# Terminal 1:
uvicorn backend.main:app --reload --port 8000

# Terminal 2:
./venv/bin/streamlit run frontend/app.py --server.port 8501
```

Check each page:
- **Home** (`/`): hero glows, stats strip, 3 feature cards hover, 4-step row
- **Get Started** (`/Get_Started`): dim grid 2-col, step badges, example code blocks
- **Evaluate & Fix** (`/Evaluate_Fix`): paste a prompt → Analyze → score grid fills, detail rows render, action cards visible
- **Settings** (`/Settings`): form inputs dark-themed, save works, success message appears
- **Nav**: active link highlights correctly on each page; "Connected" pill green when backend is up

- [ ] **Step 4: Final commit**

```bash
git add .gitignore
git commit -m "feat(ui): Glass Premium redesign complete — top nav, no sidebar, SVG icons, animations"
```
