import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import apply_styles, page_header

apply_styles()

# ── sidebar branding ───────────────────────────────────────────────────────────
st.sidebar.markdown(
    "<h2 style='margin-top:0;font-size:1.2rem;letter-spacing:-0.01em;'>ClimateRsk AI</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='font-size:0.78rem;color:#94a3b8;margin-top:-0.5rem;'>ESG-Enhanced Risk Modeling</p>",
    unsafe_allow_html=True,
)

# ── session-state defaults ─────────────────────────────────────────────────────
for _key, _val in [
    ("data_uploaded", False),
    ("models_trained", False),
    ("financial_data", None),
    ("processed_data", None),
    ("models", {}),
    ("model_results", {}),
    ("saved_portfolios", {}),
    ("saved_model_snapshots", {}),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _val

# ── hero banner ────────────────────────────────────────────────────────────────
page_header(
    "Climate-Aware Quantitative Risk Modeling",
    "Integrate ESG and climate indicators into financial risk predictions using machine learning.",
)

# ── platform status cards ──────────────────────────────────────────────────────
data_ok   = st.session_state.data_uploaded
models_ok = st.session_state.models_trained

c1, c2, c3 = st.columns(3)
with c1:
    color  = "#dcfce7" if data_ok else "#f1f5f9"
    text_c = "#15803d" if data_ok else "#64748b"
    label  = "Data Loaded" if data_ok else "Awaiting Data"
    border = "#bbf7d0" if data_ok else "#e2e8f0"
    st.markdown(f"""
    <div style='background:{color};border-radius:10px;padding:1.1rem 1.3rem;border:1px solid {border}'>
        <div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.07em;color:{text_c};margin-bottom:0.3rem;'>Data Status</div>
        <div style='font-size:1.15rem;font-weight:600;color:{text_c};'>{label}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    color  = "#dcfce7" if models_ok else "#f1f5f9"
    text_c = "#15803d" if models_ok else "#64748b"
    label  = "Models Trained" if models_ok else "Models Pending"
    border = "#bbf7d0" if models_ok else "#e2e8f0"
    st.markdown(f"""
    <div style='background:{color};border-radius:10px;padding:1.1rem 1.3rem;border:1px solid {border}'>
        <div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.07em;color:{text_c};margin-bottom:0.3rem;'>Model Status</div>
        <div style='font-size:1.15rem;font-weight:600;color:{text_c};'>{label}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    ready  = data_ok and models_ok
    color  = "#dbeafe" if ready else "#f1f5f9"
    text_c = "#1e40af" if ready else "#64748b"
    label  = "Ready for Analysis" if ready else "Setup Required"
    border = "#bfdbfe" if ready else "#e2e8f0"
    st.markdown(f"""
    <div style='background:{color};border-radius:10px;padding:1.1rem 1.3rem;border:1px solid {border}'>
        <div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.07em;color:{text_c};margin-bottom:0.3rem;'>Analysis Status</div>
        <div style='font-size:1.15rem;font-weight:600;color:{text_c};'>{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Get Started — Upload Data", type="primary"):
    st.switch_page("pages/1_Data_Upload.py")

st.markdown("---")

# ── objectives & methodology ───────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Project Objectives")
    st.markdown("""
    - Investigate how climate and ESG factors affect financial risk
    - Develop machine learning models for enhanced risk analytics
    - Demonstrate improved predictions with ESG integration
    - Identify which climate variables most influence default risk
    - Validate model performance with rigorous statistical methods
    """)
with col2:
    st.markdown("### Methodology")
    st.markdown("""
    - **Data Integration** — Combine financial data with ESG indicators
    - **Model Training** — Random Forest and Gradient Boosting algorithms
    - **Performance Comparison** — With vs. without ESG factors
    - **Statistical Validation** — AUC, Precision, Recall, F1 metrics
    - **Feature Analysis** — Climate variable importance ranking
    """)

# ── quick-start steps ──────────────────────────────────────────────────────────
st.markdown("### Quick Start Guide")
steps = [
    ("1", "Upload Data",     "Provide a financial CSV or use the built-in sample dataset."),
    ("2", "Train Models",    "Configure and train Random Forest, Gradient Boosting, or Logistic Regression models."),
    ("3", "Compare Models",  "Evaluate performance metrics and ESG lift across all trained models."),
    ("4", "Risk Dashboard",  "Explore predictions, sector breakdowns, and climate variable impact."),
    ("5", "Export Results",  "Download predictions or save portfolios to the session database."),
]
step_cols = st.columns(5)
for col, (num, title, desc) in zip(step_cols, steps):
    with col:
        st.markdown(f"""
        <div class='card' style='text-align:center;padding:1.2rem 1rem;'>
            <div style='font-size:1.5rem;font-weight:800;color:#2563eb;background:#eff6ff;
                        border-radius:50%;width:2.2rem;height:2.2rem;
                        line-height:2.2rem;margin:0 auto 0.6rem;'>{num}</div>
            <div style='font-weight:600;font-size:0.88rem;color:#0f172a;margin-bottom:0.4rem;'>{title}</div>
            <div style='font-size:0.78rem;color:#64748b;line-height:1.4;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── data structure info ────────────────────────────────────────────────────────
with st.expander("Expected Data Structure"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        **Financial Variables**
        - Portfolio values, annual returns, volatility
        - Credit scores and default indicators
        - Market data — prices, volumes, beta, P/E ratio
        """)
    with col_b:
        st.markdown("""
        **ESG / Climate Variables** *(auto-generated if absent)*
        - Carbon exposure scores and green investment ratio
        - ESG, governance, and social scores
        - Climate risk index and water stress indicators
        """)
