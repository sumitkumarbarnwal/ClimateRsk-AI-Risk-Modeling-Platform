import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── global reset ─────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* ── sidebar ──────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #cbd5e1 !important;
        font-size: 0.92rem;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #334155 !important;
    }

    /* ── page header banner ───────────────────────────────── */
    .page-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a5276 50%, #0f766e 100%);
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        color: white;
    }
    .page-header h1 {
        font-size: 1.9rem;
        font-weight: 700;
        color: white !important;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .page-header p {
        font-size: 0.95rem;
        color: #bfdbfe;
        margin: 0;
        line-height: 1.5;
    }

    /* ── section divider titles ───────────────────────────── */
    h2, h3 {
        color: #1e293b !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }
    h3 {
        border-left: 4px solid #2563eb;
        padding-left: 0.75rem;
        margin-top: 1.5rem !important;
    }

    /* ── metric cards ─────────────────────────────────────── */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.10);
    }
    [data-testid="metric-container"] label {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748b !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }

    /* ── buttons ──────────────────────────────────────────── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 8px rgba(37,99,235,0.35) !important;
        transition: all 0.2s !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        box-shadow: 0 4px 14px rgba(37,99,235,0.45) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #94a3b8 !important;
        background: #f8fafc !important;
    }
    .stButton > button:not([kind]) {
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* ── cards (custom) ───────────────────────────────────── */
    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }
    .card-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    .card-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
    }

    /* ── status badges ────────────────────────────────────── */
    .badge-success {
        display: inline-block;
        background: #dcfce7;
        color: #15803d;
        border-radius: 20px;
        padding: 0.25rem 0.8rem;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-warning {
        display: inline-block;
        background: #fef9c3;
        color: #92400e;
        border-radius: 20px;
        padding: 0.25rem 0.8rem;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-info {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        border-radius: 20px;
        padding: 0.25rem 0.8rem;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* ── stat row ─────────────────────────────────────────── */
    .stat-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .stat-item {
        flex: 1;
        min-width: 120px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .stat-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 0.2rem;
    }

    /* ── alerts / info boxes ──────────────────────────────── */
    .stAlert {
        border-radius: 10px !important;
        border-width: 1px !important;
    }
    [data-testid="stInfoMessage"],
    [data-testid="stSuccessMessage"],
    [data-testid="stWarningMessage"],
    [data-testid="stErrorMessage"] {
        border-radius: 10px !important;
        font-size: 0.9rem !important;
    }

    /* ── dataframe ────────────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e2e8f0 !important;
    }

    /* ── selectbox / multiselect / slider ─────────────────── */
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stNumberInput label, .stTextInput label, .stRadio label {
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        color: #374151 !important;
    }
    .stSlider [data-testid="stSlider"] > div > div > div {
        background: #2563eb;
    }

    /* ── expander ─────────────────────────────────────────── */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #1e293b !important;
        background: #f8fafc !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        border: 1px solid #e2e8f0 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ── progress bar ─────────────────────────────────────── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2563eb, #0f766e) !important;
        border-radius: 4px;
    }

    /* ── file uploader ────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1 !important;
        border-radius: 12px !important;
        background: #f8fafc !important;
        transition: border-color 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #2563eb !important;
    }

    /* ── divider ──────────────────────────────────────────── */
    hr {
        border-color: #e2e8f0 !important;
        margin: 1.5rem 0 !important;
    }

    /* ── hide default Streamlit footer ───────────────────── */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    sub = f'<p>{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {sub}
    </div>
    """, unsafe_allow_html=True)


def section_title(text: str):
    st.markdown(f"### {text}")


def status_badge(text: str, kind: str = "info"):
    st.markdown(f'<span class="badge-{kind}">{text}</span>', unsafe_allow_html=True)
