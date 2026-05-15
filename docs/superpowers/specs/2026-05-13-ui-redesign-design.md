# PEF UI Redesign — Design Spec
**Date:** 2026-05-13  
**Status:** Approved

## Summary

Full visual overhaul of the Streamlit frontend. Replace sidebar navigation with a sticky top nav bar. Apply a Glass Premium aesthetic: dark background (`#09090e`), animated radial glows, glassmorphism cards, gradient score numbers, SVG-only icons (no emoji), and entry animations throughout. All 4 pages are redesigned.

---

## Navigation

- **Structure:** Sticky top nav bar, no sidebar. `initial_sidebar_state="collapsed"` + CSS to hide sidebar entirely.
- **Logo:** Hexagon SVG mark + "PEF" wordmark, left-aligned.
- **Links (4 items):** Home · Get Started · Evaluate & Fix · Settings — each with a unique SVG icon, active state highlight.
- **Right side:** "Connected" status pill with animated green pulse dot (live backend check).
- **Style:** `background: rgba(9,9,14,0.8)`, `backdrop-filter: blur(20px)`, `border-bottom: 1px solid rgba(255,255,255,0.07)`.

---

## Design Tokens

| Token | Value |
|---|---|
| Background | `#09090e` |
| Card surface | `rgba(255,255,255,0.04)` |
| Card border | `rgba(255,255,255,0.09)` |
| Brand red | `#FF3621` |
| Good score | `#4ade80` |
| Warn score | `#fbbf24` |
| Bad score | `#f87171` |
| Body font | Inter |
| Mono font | JetBrains Mono (scores, prompt textarea, char count) |
| Border radius (cards) | 16px |
| Border radius (buttons) | 9–10px |

---

## Page: Home (`app.py`)

- **Hero section:** full-width, centered. Animated radial glows (red, indigo, teal) that drift. Subtle grid texture (masked radial gradient). Hero badge pill. Large 56px headline with gradient "scored instantly." Subtitle text. Two CTA buttons.
- **Stats strip:** 4 stat items separated by vertical rules — 8 dimensions · 1–10 · 3 variants · 360° safety.
- **Feature cards (3-col grid):** Evaluate · Fix · Stress/Hallucination. Each with icon-lit background (12px radius), title, description, "→" CTA link. Hover: lift + border brighten.
- **How it works:** 4-step row with numbered red circles connected by a gradient line. Step title + description below.

---

## Page: Get Started (`1_Get_Started.py`)

- Top nav (shared CSS).
- Page header: title + subtitle.
- **What is PEF:** glass card with body text.
- **How It Works:** glass card with 6 numbered step rows (SVG number badge, bold label, description).
- **Dimensions grid (2-col):** 8 dim cards, each with red-tinted background, dim name in brand red, description in muted text.
- **Example prompts:** glass card with before/after code blocks styled with mono font, no Streamlit expanders (use custom HTML `<details>` with glass styling).
- **Setup steps:** glass card, 4 icon+text rows.

---

## Page: Evaluate & Fix (`2_Evaluate_Fix.py`)

- Top nav + page header.
- **Prompt input card:** glass card, JetBrains Mono textarea, `caret-color: #FF3621`, footer row with action buttons + char count.
- **Buttons:** Primary (red gradient + glow shadow) · Ghost (glass border). No default Streamlit button styles; fully overridden via CSS.
- **Score overview:** glass card with overall score (48px mono gradient number) + 4×2 score grid. Each cell: large score number (color-coded), dimension name, animated fill bar (2px). Clicking a cell expands detail.
- **Dimension detail:** table-style rows — score badge (36px rounded square), dimension name, issues column, suggestions column. Warn rows have a subtle amber tint background.
- **Action cards (3-col):** Fix & Improve · Stress Test · Hallucination Check. Each with icon-lit background, title, description. Fix card has a red-tinted border (primary action).
- **Fix result area:** glass card, monospace textarea for fixed prompt, before/after comparison table (same token colours).
- **Progress/status:** Custom styled `st.status` with glass card wrapper.

---

## Page: Settings (`3_Settings.py`)

- Top nav + page header.
- **Databricks Connection:** glass card wrapping the form. Styled text inputs (dark background, red focus ring).
- **Token status badge:** green (set) / amber (missing) pill.
- **Evaluation Defaults:** glass card with toggle rows and select inputs. Two-column layout preserved.
- All `st.form_submit_button` → overridden to primary button style.

---

## CSS Architecture

- **Shared base CSS:** extracted into a `_shared_styles()` helper function in each page (or a shared import) — resets, fonts, top nav, button overrides, glass card classes, score colour system.
- **Sidebar suppression:** `[data-testid="stSidebar"] { display: none !important; }` + `initial_sidebar_state="collapsed"`.
- **Animations:** `@keyframes fadeUp` (staggered on page sections), `@keyframes pulse` (status dot), score bar fill transition (1s cubic-bezier).
- **No emoji anywhere** — all icons are inline SVG via `unsafe_allow_html=True` or CSS `content`.

---

## Out of Scope

- Backend changes (zero).
- Test changes.
- Any new features — purely visual.
