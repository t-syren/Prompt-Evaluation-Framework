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
  color: #e2e8f0 !important;
}}
.stApp {{
  background:
    radial-gradient(ellipse 60% 40% at 15% 0%, rgba(255,54,33,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 85% 20%, rgba(99,102,241,0.10) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 60% 90%, rgba(6,182,212,0.07) 0%, transparent 60%),
    #09090e !important;
}}

/* ── Hide ALL Streamlit chrome ── */
[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
[data-testid="stHeader"] {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stStatusWidget"] {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}
header {{ display: none !important; }}

/* ── Streamlit layout reset ── */
.main .block-container,
.stMainBlockContainer,
div.block-container,
[data-testid="stMainBlockContainer"] {{
  padding-top: 52px !important;
  margin-top: 0 !important;
  padding-left: 28px !important;
  padding-right: 28px !important;
  padding-bottom: 80px !important;
  max-width: 100% !important;
}}
.main, section[data-testid="stMain"] {{
  padding-top: 0 !important;
  margin-top: 0 !important;
}}
[data-testid="stAppViewContainer"] {{
  padding-top: 0 !important;
}}

/* ── TOP NAV — fixed to viewport top, above everything ── */
.topnav {{
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 999999;
  height: 52px;
  background: rgba(9,9,14,0.92);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.07);
  display: flex; align-items: center;
  padding: 0 28px;
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

/* Streamlit toggle */
[data-testid="stToggle"] > label > div[data-checked="true"] {{
  background-color: #FF3621 !important;
}}
[data-testid="stToggle"] > label > div {{
  background-color: rgba(255,255,255,0.15) !important;
}}
[data-testid="stToggle"] > p {{
  color: rgba(255,255,255,0.7) !important;
}}

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
"""


def nav_close() -> str:
    return ""
