"""
Deep Research Desk - Streamlit UI for the multi-agent research application.

Put this file next to agents.py, pipeline.py and tools.py, then run:
    streamlit run app.py

Pick a theme (Aurora / Daylight / Sunset) from the sidebar.
"""

import time
from datetime import datetime

import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from agents import (
    build_reader_agent,
    build_search_agent,
    critic_chain,
    writer_chain,
)

st.set_page_config(
    page_title="Deep Research Desk",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Themes
# ----------------------------------------------------------------------------
THEMES = {
    "Aurora": {  # dark, violet + cyan
        "bg": "#0B1020", "bg2": "#10172E", "surface": "#151D3A", "surface2": "#1E2850",
        "border": "#2F3C73", "text": "#EEF2FF", "muted": "#A9B4DA",
        "accent": "#8B6CFF", "accent2": "#22D3EE", "on_accent": "#FFFFFF",
        "ok": "#34D399", "err": "#FB7185",
        "hero": "linear-gradient(120deg,#4F46E5 0%,#7C3AED 50%,#0EA5E9 100%)",
        "glow": "rgba(139,108,255,.22)",
    },
    "Daylight": {  # light, indigo + teal
        "bg": "#EEF2FF", "bg2": "#E3EAFF", "surface": "#FFFFFF", "surface2": "#F1F4FF",
        "border": "#CBD5F5", "text": "#16204A", "muted": "#55628C",
        "accent": "#4F46E5", "accent2": "#0891B2", "on_accent": "#FFFFFF",
        "ok": "#059669", "err": "#DC2626",
        "hero": "linear-gradient(120deg,#4F46E5 0%,#6366F1 45%,#06B6D4 100%)",
        "glow": "rgba(79,70,229,.18)",
    },
    "Sunset": {  # dark, rose + amber
        "bg": "#1A1022", "bg2": "#22142D", "surface": "#2A1A38", "surface2": "#38224A",
        "border": "#5A3A74", "text": "#FFF1F5", "muted": "#D2B4CE",
        "accent": "#FF6B8B", "accent2": "#FFB454", "on_accent": "#2A0A14",
        "ok": "#5EEAA8", "err": "#FF8A80",
        "hero": "linear-gradient(120deg,#E11D74 0%,#F43F5E 45%,#F59E0B 100%)",
        "glow": "rgba(255,107,139,.22)",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "Aurora"
P = THEMES[st.session_state.theme]

ROOT_VARS = (
    ":root{"
    f"--bg:{P['bg']};--bg2:{P['bg2']};--surface:{P['surface']};--surface2:{P['surface2']};"
    f"--border:{P['border']};--text:{P['text']};--muted:{P['muted']};"
    f"--accent:{P['accent']};--accent2:{P['accent2']};--on-accent:{P['on_accent']};"
    f"--ok:{P['ok']};--err:{P['err']};--hero:{P['hero']};--glow:{P['glow']};"
    "}"
)

STATIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap');
html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: radial-gradient(1200px 500px at 15% -10%, var(--glow), transparent 60%), var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', system-ui, sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"], #MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1.6rem; padding-bottom: 4rem; max-width: 1100px; }
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp h5, .stApp h6, .stApp td, .stApp th, [data-testid="stMarkdownContainer"] { color: var(--text) !important; }
.stApp a { color: var(--accent2) !important; }
.stApp code { background: var(--surface2) !important; color: var(--accent2) !important; border-radius: 6px; }
.stApp pre { background: var(--surface2) !important; border: 1px solid var(--border); border-radius: 10px; }
[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
hr { border-color: var(--border) !important; }

.hero { background: var(--hero); border-radius: 20px; padding: 2.2rem 2.4rem; margin-bottom: 1.4rem;
  box-shadow: 0 18px 50px -18px var(--glow), 0 2px 0 rgba(255,255,255,.18) inset; }
.hero h1 { font-family: 'Source Serif 4', Georgia, serif; font-weight: 700; font-size: 2.7rem;
  line-height: 1.08; letter-spacing: -0.02em; margin: 0 0 .55rem 0; color: #FFFFFF !important; }
.hero p { color: rgba(255,255,255,.92) !important; font-size: 1.08rem; max-width: 56ch; margin: 0 0 1.1rem 0; }
.chips { display: flex; flex-wrap: wrap; gap: .5rem; }
.chip { background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.35); color: #FFFFFF;
  padding: .3rem .8rem; border-radius: 999px; font-size: .84rem; font-weight: 500; backdrop-filter: blur(4px); }

[data-testid="stForm"] { background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
  padding: 1.3rem 1.4rem 1.1rem 1.4rem; box-shadow: 0 10px 30px -18px var(--glow); }
div[data-baseweb="input"], div[data-baseweb="base-input"] { background: var(--bg2) !important;
  border: 1.5px solid var(--border) !important; border-radius: 12px !important; }
div[data-baseweb="input"]:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 4px var(--glow) !important; }
.stTextInput input { background: var(--bg2) !important; color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important; caret-color: var(--accent2) !important;
  font-size: 1.12rem !important; padding: 1rem 1.1rem !important; }
.stTextInput input::placeholder { color: var(--muted) !important; -webkit-text-fill-color: var(--muted) !important; opacity: .85; }

.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  background: var(--surface) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important;
  border-radius: 12px !important; font-weight: 500; transition: all .15s ease; }
.stButton > button p, .stDownloadButton > button p, [data-testid="stFormSubmitButton"] > button p { color: inherit !important; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color: var(--accent) !important;
  background: var(--surface2) !important; transform: translateY(-1px); }
[data-testid="stFormSubmitButton"] > button { background: linear-gradient(120deg, var(--accent), var(--accent2)) !important;
  color: var(--on-accent) !important; border: none !important; font-weight: 600; padding: .7rem 1.2rem; }
[data-testid="stFormSubmitButton"] > button:hover { filter: brightness(1.08); transform: translateY(-1px); }
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible,
[data-testid="stFormSubmitButton"] > button:focus-visible { outline: 2px solid var(--accent2) !important; outline-offset: 2px; }

.tracker { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 1.4rem 0 1.6rem 0; }
.stage { background: var(--surface); border: 1px solid var(--border); border-top: 4px solid var(--border);
  border-radius: 14px; padding: 1rem 1.05rem; display: flex; gap: .8rem; align-items: flex-start; }
.stage .badge { flex: 0 0 auto; width: 2rem; height: 2rem; border-radius: 50%; background: var(--surface2);
  color: var(--muted); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .95rem;
  border: 1.5px solid var(--border); }
.stage .name { font-weight: 600; font-size: 1rem; color: var(--text); }
.stage .role { color: var(--muted); font-size: .82rem; line-height: 1.4; margin-top: .15rem; }
.stage .state { margin-top: .55rem; font-size: .82rem; font-weight: 600; color: var(--muted); }
.stage.running { border-top-color: var(--accent2); box-shadow: 0 0 0 3px var(--glow); }
.stage.running .badge { background: var(--accent2); color: #04222B; border-color: var(--accent2); animation: pulse 1.2s ease-in-out infinite; }
.stage.running .state { color: var(--accent2); }
.stage.done { border-top-color: var(--ok); }
.stage.done .badge { background: var(--ok); color: #05261A; border-color: var(--ok); }
.stage.done .state { color: var(--ok); }
.stage.error { border-top-color: var(--err); }
.stage.error .badge { background: var(--err); color: #2A0A0A; border-color: var(--err); }
.stage.error .state { color: var(--err); }
@keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.14); } }
@media (prefers-reduced-motion: reduce) { .stage.running .badge { animation: none; } }
@media (max-width: 800px) { .tracker { grid-template-columns: 1fr 1fr; } .hero h1 { font-size: 2rem; } }

div[data-testid="stVerticalBlockBorderWrapper"] { background: var(--surface) !important;
  border-color: var(--border) !important; border-radius: 16px !important; }
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] h1,
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] h2,
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] h3 { font-family: 'Source Serif 4', Georgia, serif; }
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] h2 { color: var(--accent2) !important; }
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] li {
  font-family: 'Source Serif 4', Georgia, serif; font-size: 1.07rem; line-height: 1.75; }

.stTabs [data-baseweb="tab-list"] { gap: 1.6rem; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] { background: transparent !important; padding: .65rem 0; }
.stTabs [data-baseweb="tab"] p { color: var(--muted) !important; font-weight: 500; }
.stTabs [aria-selected="true"] p { color: var(--accent2) !important; font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--accent2) !important; }
.stTabs [data-baseweb="tab-border"] { background: var(--border) !important; }

.meta { color: var(--muted); font-size: .92rem; margin: 0 0 .9rem 0; }
.meta b { color: var(--text); font-weight: 600; }
[data-testid="stAlert"] { background: var(--surface) !important; border: 1px solid var(--border); border-radius: 12px; }
[data-testid="stAlert"] p { color: var(--text) !important; }

[data-testid="stSidebar"], [data-testid="stSidebar"] > div { background: var(--surface) !important; }
[data-testid="stSidebar"] { border-right: 1px solid var(--border); }
[data-testid="stSidebar"] h3 { font-family: 'Source Serif 4', Georgia, serif; }
[data-testid="stSidebar"] [role="radiogroup"] label { background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: .25rem .7rem; margin-right: .3rem; }
"""

css = ROOT_VARS + STATIC_CSS
css = "\n".join(line for line in css.splitlines() if line.strip())  # no blank lines
st.markdown(f"<style>\n{css}\n</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Pipeline (same steps as pipeline.py, but reports progress to the UI)
# ----------------------------------------------------------------------------
STAGES = [
    ("Search", "Finds recent, reliable sources on your topic."),
    ("Read", "Picks the best source and scrapes it for depth."),
    ("Write", "Drafts a report from everything gathered."),
    ("Critique", "Reviews the report and flags weaknesses."),
]


def to_text(content) -> str:
    """Agent messages can be a string or a list of content blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            parts.append(block.get("text", "") if isinstance(block, dict) else str(block))
        return "\n".join(p for p in parts if p)
    return str(content)


def render_tracker(placeholder, states, notes=None):
    labels = {"pending": "Waiting", "running": "Working…", "done": "Done", "error": "Failed"}
    marks = {"done": "✓", "error": "!"}
    notes = notes or {}
    html = '<div class="tracker">'
    for n, ((name, role), state) in enumerate(zip(STAGES, states), start=1):
        extra = f" · {notes[name]}" if name in notes else ""
        mark = marks.get(state, str(n))
        html += (
            f'<div class="stage {state}"><div class="badge">{mark}</div><div>'
            f'<div class="name">{name}</div><div class="role">{role}</div>'
            f'<div class="state">{labels[state]}{extra}</div></div></div>'
        )
    html += "</div>"
    placeholder.markdown(html, unsafe_allow_html=True)


def run_pipeline_with_ui(topic: str, tracker_slot) -> dict:
    state = {}
    states = ["pending"] * 4
    notes = {}

    def set_stage(i, value):
        states[i] = value
        render_tracker(tracker_slot, states, notes)

    render_tracker(tracker_slot, states)
    current = 0

    try:
        # Step 1 - search
        current = 0
        set_stage(0, "running")
        t = time.time()
        search_agent = build_search_agent()
        result = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        state["search_results"] = to_text(result["messages"][-1].content)
        notes["Search"] = f"{time.time() - t:.0f}s"
        set_stage(0, "done")

        # Step 2 - read
        current = 1
        set_stage(1, "running")
        t = time.time()
        reader_agent = build_reader_agent()
        result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )
        state["scraped_content"] = to_text(result["messages"][-1].content)
        notes["Read"] = f"{time.time() - t:.0f}s"
        set_stage(1, "done")

        # Step 3 - write
        current = 2
        set_stage(2, "running")
        t = time.time()
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = to_text(writer_chain.invoke({"topic": topic, "research": research_combined}))
        notes["Write"] = f"{time.time() - t:.0f}s"
        set_stage(2, "done")

        # Step 4 - critique
        current = 3
        set_stage(3, "running")
        t = time.time()
        state["feedback"] = to_text(critic_chain.invoke({"report": state["report"]}))
        notes["Critique"] = f"{time.time() - t:.0f}s"
        set_stage(3, "done")

    except Exception as exc:
        set_stage(current, "error")
        state["error"] = f"{STAGES[current][0]} stage failed: {exc}"

    return state


# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
st.session_state.setdefault("history", [])
st.session_state.setdefault("topic_input", "")
st.session_state.setdefault("active", None)

EXAMPLES = [
    "Solid-state batteries for electric vehicles",
    "mRNA vaccines beyond COVID-19",
    "State of quantum error correction",
]


def set_topic(value: str):
    st.session_state.topic_input = value


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Theme")
    st.radio("Theme", list(THEMES), key="theme", horizontal=True, label_visibility="collapsed")

    st.markdown("### Past reports")
    if not st.session_state.history:
        st.caption("Reports you generate in this session will appear here.")
    for i in reversed(range(len(st.session_state.history))):
        item = st.session_state.history[i]
        label = item["topic"][:40] + ("…" if len(item["topic"]) > 40 else "")
        if st.button(label, key=f"hist_{i}", use_container_width=True):
            st.session_state.active = i
            st.rerun()
        st.caption(item["time"])

    if st.session_state.history:
        if st.button("Clear history", use_container_width=True):
            st.session_state.history = []
            st.session_state.active = None
            st.rerun()

    st.markdown("---")
    st.caption(
        "Four agents work in sequence: search, read, write and critique. "
        "A full run usually takes a minute or two."
    )

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="hero"><h1>Deep Research Desk</h1>'
    "<p>Enter a topic. Four agents search the web, read the best source, "
    "write a report and critique it.</p>"
    '<div class="chips"><span class="chip">🔎 Live web search</span>'
    '<span class="chip">📖 Deep source reading</span>'
    '<span class="chip">✍️ Full written report</span>'
    '<span class="chip">🧐 Critic review</span></div></div>',
    unsafe_allow_html=True,
)

with st.form("research_form", border=False):
    topic = st.text_input(
        "Research topic",
        key="topic_input",
        placeholder="e.g. Impact of microplastics on marine food chains",
        label_visibility="collapsed",
    )
    f1, f2 = st.columns([1, 3])
    with f1:
        run_clicked = st.form_submit_button("Start research", use_container_width=True)
    with f2:
        st.caption("Press Enter or click Start research.")

st.caption("Not sure where to start? Try one of these:")
ex_cols = st.columns(len(EXAMPLES))
for col, ex in zip(ex_cols, EXAMPLES):
    col.button(ex, key=f"ex_{ex}", on_click=set_topic, args=(ex,), use_container_width=True)

tracker_slot = st.empty()

if run_clicked:
    if not topic.strip():
        st.warning("Enter a topic to research.")
    else:
        result = run_pipeline_with_ui(topic.strip(), tracker_slot)
        st.session_state.history.append(
            {
                "topic": topic.strip(),
                "time": datetime.now().strftime("%d %b %Y, %H:%M"),
                "result": result,
            }
        )
        st.session_state.active = len(st.session_state.history) - 1
        st.rerun()

# ----------------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------------
active = st.session_state.active
if active is not None and active < len(st.session_state.history):
    record = st.session_state.history[active]
    res = record["result"]

    keys = ("search_results", "scraped_content", "report", "feedback")
    done_states = ["done" if k in res else "pending" for k in keys]
    if "error" in res and "pending" in done_states:
        done_states[done_states.index("pending")] = "error"
    render_tracker(tracker_slot, done_states)

    st.markdown(
        f'<div class="meta">Topic: <b>{record["topic"]}</b> · {record["time"]}</div>',
        unsafe_allow_html=True,
    )

    if "error" in res:
        st.error(
            f"{res['error']}\n\nCheck the API keys in `.env` and your network "
            "connection, then run again. Completed stages are still shown below."
        )

    tab_report, tab_critic, tab_sources, tab_scraped = st.tabs(
        ["Report", "Critic feedback", "Search results", "Scraped source"]
    )

    with tab_report:
        if "report" in res:
            st.download_button(
                "Download report (.md)",
                data=res["report"],
                file_name=f"report_{record['topic'][:30].strip().replace(' ', '_')}.md",
                mime="text/markdown",
            )
            with st.container(border=True):
                st.markdown(res["report"])
        else:
            st.info("The report was not produced for this run.")

    with tab_critic:
        if "feedback" in res:
            with st.container(border=True):
                st.markdown(res["feedback"])
        else:
            st.info("No critic feedback for this run.")

    with tab_sources:
        if "search_results" in res:
            with st.container(border=True):
                st.markdown(res["search_results"])
        else:
            st.info("No search results for this run.")

    with tab_scraped:
        if "scraped_content" in res:
            with st.container(border=True):
                st.markdown(res["scraped_content"])
        else:
            st.info("No scraped content for this run.")
else:
    st.markdown(
        '<div class="meta" style="margin-top:1.5rem">'
        "Your report will appear here once the four stages finish.</div>",
        unsafe_allow_html=True,
    )