# frontend/styles.py
_FONTS = (
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900"
    "&family=JetBrains+Mono:wght@400;500;600&display=swap"
)



_LOGO_B64 = "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"

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
[data-testid="stSidebar"] {{
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
  max-width: 0 !important;
  overflow: hidden !important;
  transition: none !important;
  animation: none !important;
}}
[data-testid="stSidebarContent"] {{
  display: none !important;
  width: 0 !important;
  overflow: hidden !important;
}}
section[data-testid="stSidebar"] {{
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
}}
[data-testid="collapsedControl"] {{ display: none !important; }}
[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
[data-testid="stSidebarNavItems"] {{ display: none !important; }}
[data-testid="stSidebarNavSeparator"] {{ display: none !important; }}
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
  display: flex; align-items: center; gap: 0;
  margin-right: 32px; text-decoration: none;
}}
.logo-pill {{
  background: white; border-radius: 7px;
  padding: 3px 10px; display: flex; align-items: center;
}}
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
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"],
[data-testid="stBaseButton-primary"] {{
  background: #FF3621 !important;
  border: none !important; color: white !important;
  -webkit-text-fill-color: white !important;
  box-shadow: 0 4px 18px rgba(255,54,33,0.45) !important;
}}
.stButton > button[kind="primary"] *,
button[data-testid="baseButton-primary"] *,
[data-testid="stBaseButton-primary"] * {{
  color: white !important;
  -webkit-text-fill-color: white !important;
}}
.stButton > button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover,
[data-testid="stBaseButton-primary"]:hover {{
  background: #FF5533 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 28px rgba(255,54,33,0.6) !important;
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
[data-testid="stTextArea"] textarea,
.stTextArea textarea {{
  background: rgba(255,255,255,0.04) !important;
  background-color: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: rgba(255,255,255,0.85) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.85) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13.5px !important; line-height: 1.65 !important;
  caret-color: #FF3621 !important;
}}
[data-testid="stTextArea"] textarea:focus,
.stTextArea textarea:focus {{
  border-color: rgba(255,54,33,0.4) !important;
  box-shadow: 0 0 0 3px rgba(255,54,33,0.1) !important;
}}
[data-testid="stTextArea"] textarea::placeholder,
.stTextArea textarea::placeholder {{
  color: rgba(255,255,255,0.2) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.2) !important;
}}
[data-testid="stTextInput"] input,
.stTextInput input,
.stTextInput > div > div > input {{
  background: rgba(255,255,255,0.04) !important;
  background-color: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 8px !important;
  color: rgba(255,255,255,0.85) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.85) !important;
  caret-color: #FF3621 !important;
}}
[data-testid="stTextInput"] input:focus,
.stTextInput input:focus,
.stTextInput > div > div > input:focus {{
  border-color: rgba(255,54,33,0.4) !important;
  box-shadow: 0 0 0 3px rgba(255,54,33,0.1) !important;
}}
[data-testid="stTextInput"] input::placeholder,
.stTextInput input::placeholder {{
  color: rgba(255,255,255,0.2) !important;
  -webkit-text-fill-color: rgba(255,255,255,0.2) !important;
}}
/* Fix browser autofill injecting white background */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {{
  -webkit-box-shadow: 0 0 0 60px #09090e inset !important;
  -webkit-text-fill-color: rgba(255,255,255,0.85) !important;
  caret-color: #FF3621 !important;
}}
[data-testid="stWidgetLabel"] p,
.stTextArea label, .stTextInput label {{
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
  <a class="nav-logo" href="/" target="_self">
    <div class="logo-pill">
      <img src="data:image/png;base64,{_LOGO_B64}" alt="Syren" height="24" style="display:block;"/>
    </div>
  </a>
  <div class="nav-divider"></div>
  <div class="nav-links">
    <a class="{_cls('home')}" href="/" target="_self">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M2 7L7 2l5 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M3.5 5.5V11a.5.5 0 00.5.5h2.5V8.5h2V11.5H11a.5.5 0 00.5-.5V5.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Home
    </a>
    <a class="{_cls('get_started')}" href="/Get_Started" target="_self">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.4"/>
        <path d="M7 4.5v3l1.5 1.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
      </svg>
      Get Started
    </a>
    <a class="{_cls('evaluate')}" href="/Evaluate_Fix" target="_self">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M3 7h3l2-4 2 8 2-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Evaluate &amp; Fix
    </a>
    <a class="{_cls('settings')}" href="/Settings" target="_self">
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


def inject_sidebar_killer() -> None:
    """Inject sidebar-hiding CSS + MutationObserver into parent <head> via iframe.
    The observer continuously suppresses the sidebar on every DOM mutation,
    preventing the white sidebar flash during page transitions."""
    import streamlit.components.v1 as components
    components.html(
        """
        <script>
        (function() {
          var HIDE_CSS = [
            '[data-testid="stSidebar"]{display:none!important;width:0!important;',
            'min-width:0!important;max-width:0!important;overflow:hidden!important;',
            'visibility:hidden!important;opacity:0!important;transition:none!important;}',
            'section[data-testid="stSidebar"]{display:none!important;width:0!important;}',
            '[data-testid="collapsedControl"]{display:none!important;visibility:hidden!important;}',
            '[data-testid="stSidebarCollapsedControl"]{display:none!important;visibility:hidden!important;}'
          ].join('');

          // Inject persistent <style> into parent <head>
          if (!parent.document.getElementById('_pef_no_sidebar')) {
            var s = parent.document.createElement('style');
            s.id = '_pef_no_sidebar';
            s.textContent = HIDE_CSS;
            parent.document.head.appendChild(s);
          }

          // Also imperatively hide on every DOM change (catches transition frames)
          function kill() {
            var sel = '[data-testid="stSidebar"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]';
            parent.document.querySelectorAll(sel).forEach(function(el) {
              el.style.setProperty('display', 'none', 'important');
              el.style.setProperty('width', '0', 'important');
              el.style.setProperty('visibility', 'hidden', 'important');
              el.style.setProperty('opacity', '0', 'important');
              el.style.setProperty('transition', 'none', 'important');
            });
          }

          kill();
          var obs = new MutationObserver(kill);
          obs.observe(parent.document.documentElement, { childList: true, subtree: true });
        })();
        </script>
        """,
        height=0,
        scrolling=False,
    )
