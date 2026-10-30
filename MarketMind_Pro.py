import os
import json
import time
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# MarketMind AI — redesigned Streamlit interface
# ---------------------------------------------------------
st.set_page_config(
    page_title="MarketMind AI | Research Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme / CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --bg: #080b16;
        --panel: rgba(18, 24, 43, .78);
        --panel-2: rgba(24, 32, 55, .82);
        --line: rgba(150, 167, 220, .16);
        --text: #edf1ff;
        --muted: #9ba8c7;
        --purple: #9b8cff;
        --cyan: #5ce1e6;
        --pink: #f58bc7;
    }

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        color: var(--text);
        background:
          radial-gradient(ellipse at 12% 4%, rgba(111, 83, 255, .20), transparent 34%),
          radial-gradient(ellipse at 88% 14%, rgba(45, 211, 220, .13), transparent 30%),
          radial-gradient(ellipse at 70% 90%, rgba(232, 104, 183, .10), transparent 35%),
          linear-gradient(135deg, #080b16 0%, #0c1223 52%, #090d1a 100%);
        background-attachment: fixed;
    }
    [data-testid="stHeader"] { background: rgba(8,11,22,.55); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(13,18,35,.98), rgba(10,14,27,.98));
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: var(--text); }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1500px; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.5px; }
    h1 { color: #f4f2ff !important; }
    h2, h3 { color: #e9e7ff !important; }
    p, label, .stMarkdown { color: #d9e0f6; }
    .muted { color: var(--muted); }

    .hero {
        position: relative; overflow: hidden;
        padding: 30px 32px; border-radius: 24px;
        border: 1px solid rgba(167,153,255,.25);
        background: linear-gradient(115deg, rgba(82,67,160,.30), rgba(23,46,77,.52) 55%, rgba(26,91,104,.22));
        box-shadow: 0 18px 60px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.07);
        margin-bottom: 22px;
    }
    .hero:after {
        content: ""; position:absolute; width:300px; height:300px; right:-90px; top:-150px;
        border-radius:50%; background:rgba(104,224,232,.13); filter:blur(5px);
    }
    .eyebrow { color:#a9a0ff; text-transform:uppercase; letter-spacing:2px; font-size:11px; font-weight:700; }
    .hero h1 { font-size: clamp(30px, 4vw, 46px); margin: 8px 0 7px; }
    .hero p { color:#bdc8e7; max-width:760px; margin-bottom:0; }
    .pill {
        display:inline-block; padding:6px 11px; border-radius:30px;
        border:1px solid rgba(92,225,230,.3); color:#8df0eb;
        background:rgba(92,225,230,.08); font-size:12px; font-weight:600;
    }
    .glass-card {
        background: linear-gradient(145deg, rgba(24,31,55,.88), rgba(15,21,39,.86));
        border:1px solid var(--line); border-radius:18px; padding:20px;
        box-shadow: 0 12px 35px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.035);
        margin-bottom:14px;
    }
    .metric {
        background:linear-gradient(145deg, rgba(31,39,68,.9), rgba(17,24,43,.9));
        border:1px solid rgba(155,140,255,.20); border-radius:17px;
        padding:17px 18px; min-height:112px;
    }
    .metric-label { color:#9eabc9; font-size:12px; text-transform:uppercase; letter-spacing:1px; }
    .metric-value { color:#f3f4ff; font:700 27px 'Space Grotesk'; margin-top:7px; }
    .metric-delta { color:#69dfc2; font-size:12px; margin-top:2px; }
    .section-kicker { color:#9d92ff; font-size:11px; font-weight:700; letter-spacing:1.6px; text-transform:uppercase; }
    .stButton > button, .stDownloadButton > button {
        border:1px solid rgba(171,155,255,.35); border-radius:11px;
        color:#fff; font-weight:700; min-height:43px;
        background:linear-gradient(110deg,#7565e8,#8d71dc 55%,#477fba);
        box-shadow:0 7px 22px rgba(117,101,232,.20);
        transition:all .2s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color:#83e7ed; transform:translateY(-2px);
        box-shadow:0 10px 26px rgba(92,225,230,.18); color:#fff;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background:rgba(9,14,29,.82) !important; color:#f0f3ff !important;
        border:1px solid rgba(151,166,214,.22) !important; border-radius:10px !important;
    }
    [data-baseweb="select"] > div {
        background:rgba(9,14,29,.82); border-color:rgba(151,166,214,.22); border-radius:10px;
    }
    .stSlider [data-testid="stThumbValue"] { color:#b6aaff; }
    [data-testid="stMetric"] {
        background:rgba(25,32,55,.72); padding:14px 16px; border-radius:14px;
        border:1px solid var(--line);
    }
    [data-testid="stTabs"] button { color:#aeb9d7; font-weight:600; }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color:#bdb2ff; border-bottom-color:#9b8cff;
    }
    [data-testid="stAlert"] { border-radius:12px; }
    hr { border-color:rgba(150,167,220,.15); }
    .step {
        border-left:3px solid #8f80f5; padding:7px 0 7px 14px; margin:8px 0;
        background:linear-gradient(90deg,rgba(143,128,245,.08),transparent);
        border-radius:0 8px 8px 0;
    }
    .step small { color:#98a6c7; }
    .footer { color:#7f8baa; text-align:center; font-size:11px; padding:24px 0 5px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
defaults = {
    "api_verified": False,
    "api_key": "",
    "runs": [],
    "active_report": None,
    "approval_status": "Pending review",
    "review_notes": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

SCENARIOS = {
    "AI customer support software": "Research the market for AI-powered customer support software, analyze published pricing tiers, compare leading vendors, and identify competitive gaps.",
    "AI coding assistants": "Analyze AI coding assistants and developer tooling, comparing capabilities, pricing, target users, integrations, and competitive positioning.",
    "Workflow automation platforms": "Research workflow automation platforms, their enterprise use cases, pricing models, integrations, and potential acquisition opportunities.",
    "Enterprise RAG & knowledge assistants": "Evaluate enterprise RAG and knowledge assistant platforms, including architecture, security, deployment options, pricing, and market gaps.",
    "AI in healthcare": "Analyze AI applications in clinical and administrative healthcare, focusing on adoption, regulation, use cases, vendors, and market opportunities.",
}

def metric_card(label, value, delta=""):
    st.markdown(
        f"""<div class="metric">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">{delta}</div></div>""",
        unsafe_allow_html=True,
    )

def make_demo_report(query, scenario, iterations, temperature, budget):
    """Creates clearly labelled sample output for UI demonstration only."""
    return {
        "id": f"MM-{datetime.now().strftime('%y%m%d-%H%M%S')}",
        "created": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "scenario": scenario,
        "query": query,
        "iterations": iterations,
        "temperature": temperature,
        "budget": budget,
        "summary": (
            "This is a demonstration report generated by the interface preview. "
            "Connect your research agents and search/retrieval tools to replace this sample "
            "with evidence-backed market findings."
        ),
        "findings": [
            {"topic": "Market landscape", "status": "Needs live research", "evidence": "No source retrieved in demo mode."},
            {"topic": "Vendor pricing", "status": "Needs verification", "evidence": "Pricing must be collected from current vendor sources."},
            {"topic": "Competitive gaps", "status": "Analyst review required", "evidence": "Requires comparison of verified vendor capabilities."},
        ],
        "qc": {
            "Unsupported claims": "Not evaluated — demo mode",
            "Missing sources": "No sources attached",
            "Coverage gaps": "Requires live plan-to-report comparison",
            "Contradictions": "Not evaluated — demo mode",
        },
        "tokens": 0,
        "cost": 0.0,
        "approval": "Pending review",
    }

def report_as_markdown(report):
    lines = [
        f"# MarketMind AI — Market Intelligence Brief",
        f"**Report ID:** {report['id']}  ",
        f"**Created:** {report['created']}  ",
        f"**Scenario:** {report['scenario']}",
        "",
        "## Client research brief",
        report["query"],
        "",
        "## Executive summary",
        report["summary"],
        "",
        "## Research findings",
    ]
    for item in report["findings"]:
        lines += [f"### {item['topic']}", f"- Status: {item['status']}", f"- Evidence: {item['evidence']}", ""]
    lines += ["## Quality control", *[f"- **{k}:** {v}" for k, v in report["qc"].items()]]
    lines += ["", f"**Approval status:** {report.get('approval', 'Pending review')}", "",
              "> Note: Demo-mode output. Connect the actual agent pipeline to generate verified findings and citations."]
    return "\n".join(lines)

# ---------- API setup gate ----------
if not st.session_state.api_verified:
    st.markdown("<div style='height:5vh'></div>", unsafe_allow_html=True)
    left, center, right = st.columns([1, 1.25, 1])
    with center:
        st.markdown(
            """
            <div class="hero" style="text-align:center">
              <div class="eyebrow">Autonomous business intelligence</div>
              <h1>🧠 MarketMind AI</h1>
              <p style="margin:auto">Your intelligent workspace for structured market research, competitive analysis and evidence-led decisions.</p>
              <br><span class="pill">RESEARCH • ANALYZE • DECIDE</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.image(
            "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85",
            use_container_width=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔐 Connect your OpenAI workspace")
        st.caption("Enter an API key to unlock the dashboard. The current starter app checks key format only; it does not make a live API verification request.")
        with st.form("api_setup_form"):
            key_input = st.text_input("OpenAI API key", type="password", placeholder="sk-...", help="Keep your API key private. Do not share it or commit it to source control.")
            submitted = st.form_submit_button("Unlock MarketMind →", use_container_width=True)
        if submitted:
            if key_input.startswith("sk-") and len(key_input) > 20:
                st.session_state.api_key = key_input
                os.environ["OPENAI_API_KEY"] = key_input
                st.session_state.api_verified = True
                st.rerun()
            else:
                st.error("The key format does not look valid. Check that it starts with sk- and try again.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🧠 MarketMind")
    st.caption("RESEARCH INTELLIGENCE PLATFORM")
    st.markdown("---")
    st.markdown("**WORKSPACE STATUS**")
    st.success("Workspace unlocked")
    st.caption("Model target: GPT-4o-mini")
    page = st.radio(
        "NAVIGATION",
        ["Overview", "Research Studio", "Quality Control", "Approval Center", "Analytics", "Research History"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**SESSION**")
    st.caption(f"Research runs: {len(st.session_state.runs)}")
    if st.button("🔒 Lock workspace", use_container_width=True):
        st.session_state.api_verified = False
        st.session_state.api_key = ""
        st.rerun()
    st.caption("API key is held in this Streamlit session. Use environment secrets for deployed apps.")

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">MARKET INTELLIGENCE • AUTONOMOUS WORKFLOWS</div>
      <h1>Think deeper. Research smarter.</h1>
      <p>Plan research, organize evidence, review quality and turn market signals into confident business decisions.</p>
      <br><span class="pill">● WORKSPACE ACTIVE</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Overview ----------
if page == "Overview":
    st.markdown("### Your research command center")
    st.caption("A unified view of your MarketMind workspace and recent activity.")
    a, b, c, d = st.columns(4)
    with a: metric_card("Research runs", str(len(st.session_state.runs)), "Saved in this session")
    with b: metric_card("Reports ready", str(sum(1 for r in st.session_state.runs if r.get("approval") == "Approved")), "Approved reports")
    with c: metric_card("Awaiting review", str(sum(1 for r in st.session_state.runs if r.get("approval") == "Pending review")), "Human approval required")
    with d: metric_card("Pipeline mode", "Preview", "Connect agent functions for live research")
    st.markdown("")
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">START HERE</div>', unsafe_allow_html=True)
        st.subheader("Launch a new research mission")
        st.write("Define a business question, choose a research scenario and configure the agent run.")
        st.image("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
        if st.button("Open Research Studio →", use_container_width=True):
            st.session_state["navigate_to_studio"] = True
            st.info("Choose **Research Studio** from the sidebar to configure your run.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">AGENT WORKFLOW</div>', unsafe_allow_html=True)
        st.subheader("How MarketMind works")
        for title, detail in [
            ("01  Understand", "Analyze the request and define scope."),
            ("02  Plan", "Break the question into research objectives."),
            ("03  Investigate", "Search, retrieve and calculate evidence."),
            ("04  Validate", "Check coverage, sources and consistency."),
            ("05  Approve", "Send the report to a human reviewer."),
        ]:
            st.markdown(f'<div class="step"><b>{title}</b><br><small>{detail}</small></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("### Recent research")
    if st.session_state.runs:
        recent = pd.DataFrame([{
            "Report ID": r["id"], "Scenario": r["scenario"], "Created": r["created"], "Status": r["approval"]
        } for r in st.session_state.runs[-5:][::-1]])
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("No research runs yet. Start your first mission in Research Studio.")

# ---------- Research Studio ----------
elif page == "Research Studio":
    st.markdown("### 🚀 Autonomous Research Studio")
    st.caption("Configure a research brief and run the current interface preview.")
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1600&q=85", use_container_width=True)
    col1, col2 = st.columns([1.35, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">01 / RESEARCH INTAKE</div>', unsafe_allow_html=True)
        scenario = st.selectbox("Research scenario", list(SCENARIOS.keys()))
        query = st.text_area("Client request / research brief", value=SCENARIOS[scenario], height=150)
        st.markdown('<div class="section-kicker">02 / AGENT CONFIGURATION</div>', unsafe_allow_html=True)
        x, y = st.columns(2)
        with x:
            iterations = st.slider("Maximum iterations", 1, 10, 5)
            temperature = st.slider("Model temperature", 0.0, 1.0, 0.2, 0.05)
        with y:
            budget = st.number_input("Cost ceiling (USD)", min_value=0.10, max_value=20.0, value=0.50, step=0.10)
            output_style = st.selectbox("Report style", ["Executive brief", "Detailed analyst report", "Competitive comparison"])
        run = st.button("⚡ Run MarketMind pipeline", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">RESEARCH PRINCIPLES</div>', unsafe_allow_html=True)
        st.subheader("Evidence before conclusions")
        st.write("MarketMind is designed to separate sourced facts from analyst interpretation and unresolved questions.")
        st.image("https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1000&q=85", use_container_width=True)
        st.markdown("**Output labels**")
        st.markdown("- 🟢 **Fact:** supported by a source")
        st.markdown("- 🟣 **Inference:** reasoned interpretation")
        st.markdown("- 🟡 **Uncertainty:** not yet verified")
        st.markdown("</div>", unsafe_allow_html=True)
    if run:
        if not query.strip():
            st.error("Please enter a research brief before running the pipeline.")
        else:
            with st.status("Running interface demonstration...", expanded=True) as status:
                stages = [
                    ("Request analyser", "Interpreting client objective and scope..."),
                    ("Research planner", "Preparing research objectives and sub-questions..."),
                    ("Tool dispatcher", "Demo mode: live search and retrieval tools are not connected..."),
                    ("Evidence analyst", "Preparing evidence-status placeholders..."),
                    ("Report synthesizer", "Assembling a sample report preview..."),
                ]
                progress = st.progress(0)
                for i, (name, detail) in enumerate(stages, start=1):
                    st.write(f"**{name}:** {detail}")
                    progress.progress(i / len(stages))
                    time.sleep(0.15)
                status.update(label="Demo pipeline finished", state="complete", expanded=False)
            report = make_demo_report(query, scenario, iterations, temperature, budget)
            report["output_style"] = output_style
            st.session_state.active_report = report
            st.session_state.runs.append(report)
            st.session_state.approval_status = "Pending review"
            st.success("Sample report created. Connect your real agent tools to produce live, source-backed research.")
    if st.session_state.active_report:
        report = st.session_state.active_report
        st.markdown("### 📄 Report preview")
        st.warning("This is a UI demonstration report, not the result of a live research run.")
        st.markdown(f"**{report['id']}** · {report['created']} · {report.get('output_style', 'Executive brief')}")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Executive summary")
        st.write(report["summary"])
        st.subheader("Research findings")
        st.dataframe(pd.DataFrame(report["findings"]), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("⬇ Download report (Markdown)", report_as_markdown(report), file_name=f"{report['id']}.md", mime="text/markdown")

# ---------- Quality Control ----------
elif page == "Quality Control":
    st.markdown("### 🛡️ Quality Control & Evidence Audit")
    st.caption("Review report integrity before it reaches the approval stage.")
    st.image("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1400&q=80", use_container_width=True)
    report = st.session_state.active_report
    if not report:
        st.info("Create a research report in Research Studio before running a quality review.")
    else:
        st.markdown(f"**Active report:** `{report['id']}`")
        st.warning("The current report is a demo. These checks describe missing live evidence; they are not a real automated audit.")
        checks = pd.DataFrame([
            {"Audit check": k, "Current result": v}
            for k, v in report["qc"].items()
        ])
        st.dataframe(checks, use_container_width=True, hide_index=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Reviewer checklist")
        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("Research question and scope are clear", key="qc_scope")
            st.checkbox("All key claims have traceable sources", key="qc_sources")
        with c2:
            st.checkbox("Pricing and dates are current", key="qc_current")
            st.checkbox("Limitations and uncertainties are disclosed", key="qc_limits")
        if st.button("Record manual QC review", use_container_width=True):
            completed = all(st.session_state.get(k, False) for k in ["qc_scope", "qc_sources", "qc_current", "qc_limits"])
            if completed:
                st.success("Checklist completed. A reviewer can now proceed to the Approval Center.")
            else:
                st.warning("Complete all checklist items before recording the review.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Approval Center ----------
elif page == "Approval Center":
    st.markdown("### ⚖️ Human Approval Center")
    st.caption("Reports should be reviewed by a person before publication.")
    st.image("https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1400&q=85", use_container_width=True)
    report = st.session_state.active_report
    if not report:
        st.info("There is no report awaiting review. Run a research task first.")
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"**Report:** `{report['id']}`")
        st.markdown(f"**Current status:** `{report.get('approval', 'Pending review')}`")
        reviewer = st.text_input("Reviewer name", placeholder="Enter reviewer name")
        notes = st.text_area("Review notes / justification", placeholder="Record evidence checks, limitations and requested changes...")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✅ Approve report", use_container_width=True):
                if reviewer.strip():
                    report["approval"] = "Approved"
                    report["reviewer"] = reviewer.strip()
                    report["review_notes"] = notes
                    st.session_state.approval_status = "Approved"
                    st.success("Report marked as approved in this session.")
                else:
                    st.error("Enter the reviewer name before approval.")
        with c2:
            if st.button("↩ Request revision", use_container_width=True):
                if notes.strip():
                    report["approval"] = "Revision requested"
                    report["reviewer"] = reviewer.strip()
                    report["review_notes"] = notes
                    st.warning("Revision request saved in this session.")
                else:
                    st.error("Add review notes explaining the requested changes.")
        with c3:
            if st.button("✕ Reject report", use_container_width=True):
                report["approval"] = "Rejected"
                report["reviewer"] = reviewer.strip()
                report["review_notes"] = notes
                st.error("Report marked as rejected in this session.")
        st.markdown("</div>", unsafe_allow_html=True)
        if report.get("review_notes"):
            st.caption(f"Latest review notes: {report['review_notes']}")

# ---------- Analytics ----------
elif page == "Analytics":
    st.markdown("### 📈 Analytics & Cost Intelligence")
    st.caption("Session-level activity and sample pipeline metrics.")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1400&q=85", use_container_width=True)
    runs = st.session_state.runs
    a, b, c, d = st.columns(4)
    with a: metric_card("Total runs", str(len(runs)), "Current session")
    with b: metric_card("Approved", str(sum(r.get("approval") == "Approved" for r in runs)), "Human-reviewed")
    with c: metric_card("Rejected", str(sum(r.get("approval") == "Rejected" for r in runs)), "Current session")
    with d: metric_card("Demo spend", "$0.00", "No API calls made by this UI")
    if runs:
        run_df = pd.DataFrame([{"Run": r["id"], "Scenario": r["scenario"], "Status": r["approval"], "Budget ($)": r["budget"]} for r in runs])
        st.markdown("#### Run activity")
        st.dataframe(run_df, use_container_width=True, hide_index=True)
        st.markdown("#### Configured budget by research run")
        st.bar_chart(run_df.set_index("Run")["Budget ($)"])
    else:
        st.info("Analytics will populate after you create research runs.")

# ---------- Research History ----------
elif page == "Research History":
    st.markdown("### 🗂️ Research History")
    st.caption("Research runs are stored in Streamlit session state and reset when the session ends.")
    if not st.session_state.runs:
        st.info("Your research history is empty. Start a run in Research Studio.")
    else:
        for report in reversed(st.session_state.runs):
            with st.expander(f"{report['id']}  ·  {report['scenario']}  ·  {report['approval']}"):
                st.caption(report["created"])
                st.write(report["query"])
                st.write(report["summary"])
                st.download_button(
                    "Download this report",
                    report_as_markdown(report),
                    file_name=f"{report['id']}.md",
                    mime="text/markdown",
                    key=f"download_{report['id']}",
                )

st.markdown('<div class="footer">MARKETMIND AI · RESEARCH WITH CLARITY, EVIDENCE AND HUMAN OVERSIGHT</div>', unsafe_allow_html=True)
