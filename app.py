"""
app.py — Multi-Agent AI Research System
Streamlit UI for the research pipeline defined in pipeline.py
Run with: streamlit run app.py
"""

import os
import json
import time
import streamlit as st

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0c0e14;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(16,185,129,0.08) 0%, transparent 60%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #12151f !important;
    border-right: 1px solid rgba(99,102,241,0.2);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select,
[data-testid="stSidebar"] .stSlider {
    background: #1e2130 !important;
    border-color: rgba(99,102,241,0.3) !important;
}

/* ── Hero title ── */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-weight: 400;
    line-height: 1.15;
    color: #f8fafc;
    letter-spacing: -0.02em;
    margin-bottom: 0.2rem;
}
.hero-title em {
    font-style: italic;
    background: linear-gradient(135deg, #818cf8 0%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    color: #94a3b8;
    font-weight: 300;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* ── Pipeline badge ── */
.pipeline-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #a5b4fc;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 1.4rem;
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2.2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.35) !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    box-shadow: 0 6px 32px rgba(99,102,241,0.55) !important;
    transform: translateY(-1px) !important;
}

/* ── Textarea / inputs ── */
.stTextArea textarea, .stTextInput input {
    background: #1a1d2e !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #12151f;
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
    border: 1px solid rgba(99,102,241,0.15);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #64748b !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.18) !important;
    color: #a5b4fc !important;
}

/* ── Code blocks ── */
.stCode, [data-testid="stCode"] {
    background: #0f1117 !important;
    border: 1px solid rgba(99,102,241,0.15) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── Section headers ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.5rem;
    padding-top: 0.8rem;
}

/* ── Metric card ── */
.metric-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(52,211,153,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    text-align: center;
    margin-bottom: 1.2rem;
}
.metric-score {
    font-family: 'DM Serif Display', serif;
    font-size: 4rem;
    line-height: 1;
    background: linear-gradient(135deg, #818cf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: 0.78rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
}

/* ── Verdict card ── */
.verdict-card {
    background: rgba(52,211,153,0.08);
    border-left: 3px solid #34d399;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: #6ee7b7;
    font-style: italic;
    font-size: 1.05rem;
}

/* ── List items ── */
.strength-item {
    background: rgba(52,211,153,0.06);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 8px;
    padding: 0.55rem 1rem;
    margin: 0.4rem 0;
    color: #d1fae5;
    font-size: 0.92rem;
}
.improvement-item {
    background: rgba(251,191,36,0.06);
    border: 1px solid rgba(251,191,36,0.2);
    border-radius: 8px;
    padding: 0.55rem 1rem;
    margin: 0.4rem 0;
    color: #fef3c7;
    font-size: 0.92rem;
}

/* ── Divider ── */
hr { border-color: rgba(99,102,241,0.12) !important; }

/* ── Step status ── */
.step-complete {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    color: #6ee7b7;
    font-size: 0.88rem;
    margin: 0.3rem 0;
}

/* ── Markdown in report tab ── */
.report-body h1, .report-body h2, .report-body h3 {
    color: #c7d2fe;
    font-family: 'DM Serif Display', serif;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def set_env_keys(openai_key: str, mistral_key: str, tavily_key: str):
    """Push sidebar keys into environment so pipeline.py picks them up."""
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if mistral_key:
        os.environ["MISTRAL_API_KEY"] = mistral_key
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key


def validate_inputs(topic, openai_key, mistral_key, tavily_key, provider):
    if not topic.strip():
        return False, "⚠️ Please enter a research topic."
    if provider == "OpenAI" and not openai_key.strip():
        return False, "⚠️ OpenAI API key is required (sidebar)."
    if provider == "Mistral" and not mistral_key.strip():
        return False, "⚠️ Mistral API key is required (sidebar)."
    if not tavily_key.strip():
        return False, "⚠️ Tavily API key is required (sidebar)."
    return True, ""


def safe_parse_critique(feedback) -> dict:
    """
    Normalise the critic output regardless of whether it arrives as
    a dict, a JSON string, or a raw string.
    """
    if isinstance(feedback, dict):
        return feedback

    if isinstance(feedback, str):
        # strip markdown fences if present
        cleaned = feedback.strip()
        for fence in ["```json", "```"]:
            cleaned = cleaned.replace(fence, "")
        cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    return {
        "score_out_of_10": "N/A",
        "strengths": [],
        "areas_for_improvement": [],
        "one_line_verdict": str(feedback),
    }


def score_color(score):
    """Return a CSS hex color based on score."""
    try:
        s = float(str(score).split("/")[0])
        if s >= 8:
            return "#34d399"
        elif s >= 6:
            return "#fbbf24"
        return "#f87171"
    except (ValueError, TypeError):
        return "#94a3b8"


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    st.markdown("**API Keys**")
    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Required for the LLM writer and critic chains.",
    )
    mistral_key = st.text_input(
        "Mistral API Key",
        type="password",
        placeholder="Optional if using OpenAI models",
        help="Required only if your pipeline uses a Mistral model.",
    )
    tavily_key = st.text_input(
        "Tavily API Key",
        type="password",
        placeholder="tvly-...",
        help="Required for the web search agent.",
    )

    st.markdown("---")
st.markdown("**Model & Search**")

provider = st.selectbox(
    "LLM Provider",
    options=["OpenAI", "Mistral"],
    index=0,
    help="Choose which LLM provider your pipeline uses.",
)

if provider == "OpenAI":
    model_choice = st.selectbox(
        "LLM Model",
        options=["gpt-4o-mini", "gpt-4.1", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
    )
else:
    model_choice = st.selectbox(
        "LLM Model",
        options=["mistral-large-latest", "mistral-small-latest", "open-mistral-7b"],
        index=0,
    )


    max_results = st.slider(
        "Max Search Results",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
        help="Number of web results the search agent fetches.",
    )

    # Expose these to the pipeline via env vars
    os.environ["RESEARCH_MODEL"] = model_choice
os.environ["RESEARCH_PROVIDER"] = provider  # ← add this
os.environ["RESEARCH_MAX_RESULTS"] = str(max_results)


st.markdown("---")
st.markdown(
        "<div style='font-size:0.75rem;color:#475569;line-height:1.6;'>"
        "Keys are stored only for this session and are never persisted."
        "</div>",
        unsafe_allow_html=True,
    )


# ── Hero header ──────────────────────────────────────────────────────────────

st.markdown(
    '<div class="pipeline-badge">🔬 &nbsp; 4-Agent Pipeline</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-title">Multi-Agent <em>AI Research</em> System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">'
    "Enter any topic and watch four specialised agents — Search, Reader, Writer, and Critic — "
    "collaborate to produce a structured, reviewed research report in seconds."
    "</div>",
    unsafe_allow_html=True,
)

# ── Topic input ──────────────────────────────────────────────────────────────

topic = st.text_area(
    "Research Topic",
    placeholder="e.g. Recent breakthroughs in quantum error correction",
    height=100,
    label_visibility="collapsed",
)

run_clicked = st.button("🚀  Run Research Pipeline", use_container_width=True)

st.markdown("---")


# ── Pipeline execution ───────────────────────────────────────────────────────

if run_clicked:
    ok, err_msg = validate_inputs(topic, openai_key, mistral_key, tavily_key, provider)
    if not ok:
        st.error(err_msg)
        st.stop()

    # Push keys to environment
    set_env_keys(openai_key, mistral_key, tavily_key)

    # Import here so env vars are set before pipeline imports them
    try:
        from pipeline import run_research_pipeline
    except ImportError as e:
        st.error(
            f"**Could not import `pipeline.py`.**\n\n"
            f"Make sure `pipeline.py` is in the same folder as `app.py`.\n\n"
            f"Details: `{e}`"
        )
        st.stop()

    # ── Stage-by-stage progress ──
    result = {}
    pipeline_error = None

    with st.status("Running research pipeline…", expanded=True) as status:
        st.write("🔍 **Step 1 — Search Agent** is fetching web results…")
        t0 = time.time()

        try:
            result = run_research_pipeline(topic)
            elapsed = time.time() - t0

            st.write(f"✅ Search complete ({elapsed:.1f}s)")
            st.write("📄 **Step 2 — Reader Agent** scraped top sources")
            st.write("✍️  **Step 3 — Writer Chain** drafted the report")
            st.write("🧐 **Step 4 — Critic Chain** reviewed the report")

            status.update(
                label=f"✅ Pipeline complete in {elapsed:.0f}s",
                state="complete",
                expanded=False,
            )

        except Exception as exc:
            pipeline_error = exc
            status.update(label="❌ Pipeline failed", state="error", expanded=True)

    if pipeline_error:
        st.error(
            f"**Pipeline error:** {pipeline_error}\n\n"
            "Check that all API keys are valid, your `pipeline.py` is correct, "
            "and all dependencies are installed."
        )
        st.stop()

    # Cache result in session state
    st.session_state["last_result"] = result
    st.session_state["last_topic"] = topic


# ── Display results ──────────────────────────────────────────────────────────

if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    cached_topic = st.session_state.get("last_topic", "")

    st.markdown(
        f"<div class='section-label'>Results for: {cached_topic}</div>",
        unsafe_allow_html=True,
    )

    tab_search, tab_reader, tab_report, tab_critique = st.tabs(
        ["🔍 Search", "📄 Reader", "📝 Report", "🧐 Critique"]
    )

    # ── Tab 1: Search ──
    with tab_search:
        st.markdown(
            "<div class='section-label'>Web search results</div>",
            unsafe_allow_html=True,
        )
        search_text = result.get("search_results", "No search results returned.")
        st.code(search_text, language=None)

    # ── Tab 2: Reader ──
    with tab_reader:
        st.markdown(
            "<div class='section-label'>Scraped & cleaned article content</div>",
            unsafe_allow_html=True,
        )
        scraped_text = result.get("scraped_content", "No scraped content returned.")
        st.code(scraped_text, language=None)

    # ── Tab 3: Report ──
    with tab_report:
        st.markdown(
            "<div class='section-label'>Generated research report</div>",
            unsafe_allow_html=True,
        )
        report_text = result.get("report", "No report generated.")

        # Render as rich markdown; wrap in a div for scoped styling
        st.markdown(
            f"<div class='report-body'></div>",
            unsafe_allow_html=True,
        )
        st.markdown(report_text)

        # Download button
        st.download_button(
            label="⬇️  Download Report (.md)",
            data=report_text,
            file_name=f"research_report_{cached_topic[:40].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    # ── Tab 4: Critique ──
    with tab_critique:
        raw_feedback = result.get("feedback") or result.get("critique", {})
        critique = safe_parse_critique(raw_feedback)

        score = critique.get("score_out_of_10", "N/A")
        strengths = critique.get("strengths", [])
        improvements = critique.get("areas_for_improvement", [])
        verdict = critique.get("one_line_verdict", "")

        # Score metric
        col_score, col_verdict = st.columns([1, 2])
        with col_score:
            st.markdown(
                f"""
                <div class='metric-card'>
                    <div class='metric-score'>{score}</div>
                    <div class='metric-label'>Score out of 10</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_verdict:
            st.markdown(
                "<div class='section-label'>One-line verdict</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='verdict-card'>\"{verdict}\"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        col_str, col_imp = st.columns(2)

        with col_str:
            st.markdown(
                "<div class='section-label'>✅ Strengths</div>",
                unsafe_allow_html=True,
            )
            if strengths:
                if isinstance(strengths, list):
                    for s in strengths:
                        st.markdown(
                            f"<div class='strength-item'>• {s}</div>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.markdown(
                        f"<div class='strength-item'>{strengths}</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No strengths listed.")

        with col_imp:
            st.markdown(
                "<div class='section-label'>⚠️ Areas for Improvement</div>",
                unsafe_allow_html=True,
            )
            if improvements:
                if isinstance(improvements, list):
                    for imp in improvements:
                        st.markdown(
                            f"<div class='improvement-item'>• {imp}</div>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.markdown(
                        f"<div class='improvement-item'>{improvements}</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No improvements listed.")

        # Raw JSON expander for debugging
        with st.expander("🔧 Raw critic JSON"):
            st.json(critique)

else:
    # Empty state illustration
    st.markdown(
        """
        <div style="text-align:center; padding: 4rem 2rem; color: #334155;">
            <div style="font-size:4rem; margin-bottom:1rem;">🔬</div>
            <div style="font-size:1.1rem; color:#475569; font-family:'DM Sans',sans-serif;">
                Enter a topic and click <strong style="color:#818cf8;">Run Research Pipeline</strong> to begin.
            </div>
            <div style="margin-top:2rem; display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
                <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:1rem 1.4rem;min-width:130px;">
                    <div style="font-size:1.6rem;">🔍</div>
                    <div style="font-size:0.8rem;color:#6366f1;margin-top:0.3rem;font-weight:600;">Search</div>
                </div>
                <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:1rem 1.4rem;min-width:130px;">
                    <div style="font-size:1.6rem;">📄</div>
                    <div style="font-size:0.8rem;color:#6366f1;margin-top:0.3rem;font-weight:600;">Read</div>
                </div>
                <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:1rem 1.4rem;min-width:130px;">
                    <div style="font-size:1.6rem;">✍️</div>
                    <div style="font-size:0.8rem;color:#6366f1;margin-top:0.3rem;font-weight:600;">Write</div>
                </div>
                <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:1rem 1.4fc;min-width:130px;">
                    <div style="font-size:1.6rem;">🧐</div>
                    <div style="font-size:0.8rem;color:#6366f1;margin-top:0.3rem;font-weight:600;">Critique</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )