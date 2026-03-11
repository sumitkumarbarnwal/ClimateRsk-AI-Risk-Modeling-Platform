import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import apply_styles, page_header

apply_styles()
page_header("Data Upload & Processing",
            "Upload a financial CSV or load the built-in synthetic dataset to get started.")

# ── helpers ──────────────────────────────────────────────────────────────────

def generate_sample_data(n: int = 500) -> pd.DataFrame:
    np.random.seed(42)
    df = pd.DataFrame({
        "company_id":       [f"COMP_{i:04d}" for i in range(n)],
        "portfolio_value":  np.random.lognormal(12, 1.5, n),
        "annual_return":    np.random.normal(0.08, 0.15, n),
        "volatility":       np.random.uniform(0.05, 0.45, n),
        "credit_score":     np.random.randint(300, 850, n),
        "debt_ratio":       np.random.uniform(0.1, 0.9, n),
        "market_cap":       np.random.lognormal(10, 2, n),
        "pe_ratio":         np.random.uniform(5, 50, n),
        "beta":             np.random.normal(1.0, 0.5, n),
        "esg_score":        np.random.uniform(0, 100, n),
        "carbon_exposure":  np.random.uniform(0, 1, n),
        "green_ratio":      np.random.uniform(0, 1, n),
        "climate_risk_idx": np.random.uniform(0, 1, n),
        "water_stress":     np.random.uniform(0, 1, n),
        "governance_score": np.random.uniform(0, 100, n),
        "social_score":     np.random.uniform(0, 100, n),
        "sector":           np.random.choice(
            ["Energy", "Finance", "Technology", "Healthcare",
             "Materials", "Utilities", "Consumer"], n),
        "region":           np.random.choice(
            ["North America", "Europe", "Asia Pacific", "Emerging Markets"], n),
    })
    # binary default label driven by credit score + carbon exposure
    risk = (
        -0.003 * df["credit_score"]
        + 0.5   * df["debt_ratio"]
        + 0.3   * df["carbon_exposure"]
        + 0.2   * df["climate_risk_idx"]
        + np.random.normal(0, 0.3, n)
    )
    df["default_risk"] = (risk > risk.median()).astype(int)
    return df


def add_synthetic_esg(df: pd.DataFrame) -> pd.DataFrame:
    n = len(df)
    np.random.seed(123)
    if "esg_score"        not in df.columns:
        df["esg_score"]        = np.random.uniform(0, 100, n)
    if "carbon_exposure"  not in df.columns:
        df["carbon_exposure"]  = np.random.uniform(0, 1, n)
    if "green_ratio"      not in df.columns:
        df["green_ratio"]      = np.random.uniform(0, 1, n)
    if "climate_risk_idx" not in df.columns:
        df["climate_risk_idx"] = np.random.uniform(0, 1, n)
    if "water_stress"     not in df.columns:
        df["water_stress"]     = np.random.uniform(0, 1, n)
    if "governance_score" not in df.columns:
        df["governance_score"] = np.random.uniform(0, 100, n)
    return df


# ── session-state defaults ────────────────────────────────────────────────────
for key, val in [
    ("data_uploaded", False),
    ("models_trained", False),
    ("financial_data", None),
    ("processed_data", None),
    ("models", {}),
    ("model_results", {}),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("**Data Options**")
data_source = st.sidebar.radio(
    "Choose data source",
    ["Upload CSV", "Use Sample Data"],
    index=1 if not st.session_state.data_uploaded else 0,
)

# ── main UI ───────────────────────────────────────────────────────────────────
if data_source == "Use Sample Data":
    st.info("Built-in synthetic dataset — 500 companies, 18 financial features + ESG indicators.")
    if st.button("Load Sample Dataset", type="primary"):
        with st.spinner("Generating sample data ..."):
            df = generate_sample_data(500)
            st.session_state.financial_data = df
            st.session_state.processed_data = df
            st.session_state.data_uploaded  = True
        st.success("Sample data loaded — 500 records ready.")
        st.rerun()

else:  # Upload CSV
    uploaded = st.file_uploader("Upload your financial CSV file", type=["csv"])
    if uploaded:
        with st.spinner("Reading file ..."):
            df = pd.read_csv(uploaded)
            df = add_synthetic_esg(df)
            if "default_risk" not in df.columns:
                num_cols = df.select_dtypes(include=np.number).columns.tolist()
                if num_cols:
                    mid = df[num_cols[0]].median()
                    df["default_risk"] = (df[num_cols[0]] > mid).astype(int)
            st.session_state.financial_data = df
            st.session_state.processed_data = df
            st.session_state.data_uploaded  = True
        st.success(f"File uploaded: {len(df):,} rows × {df.shape[1]} columns")
        st.rerun()

# ── show data preview once loaded ─────────────────────────────────────────────
if st.session_state.data_uploaded and st.session_state.financial_data is not None:
    df = st.session_state.financial_data

    st.markdown("### Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records",  f"{len(df):,}")
    col2.metric("Total Features", df.shape[1])
    col3.metric("Default Rate",
                f"{df['default_risk'].mean()*100:.1f}%" if "default_risk" in df.columns else "N/A")
    col4.metric("Missing Values", int(df.isnull().sum().sum()))

    st.markdown("### Column Summary")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Numeric columns**")
        num = df.select_dtypes(include=np.number)
        st.dataframe(num.describe().round(3), use_container_width=True)
    with col_b:
        st.markdown("**Column types**")
        dtype_df = pd.DataFrame(
            {"Type": df.dtypes.astype(str), "Non-Null": df.notnull().sum()}
        )
        st.dataframe(dtype_df, use_container_width=True)

    # ESG columns present?
    esg_cols = [c for c in ["esg_score","carbon_exposure","green_ratio",
                             "climate_risk_idx","water_stress","governance_score"]
                if c in df.columns]
    if esg_cols:
        st.markdown("### ESG Indicator Summary")
        st.dataframe(df[esg_cols].describe().round(3), use_container_width=True)

    st.success("Data ready — proceed to Model Training in the sidebar.")
else:
    if data_source == "Upload CSV":
        st.info("Upload a CSV file to begin, or switch to Use Sample Data in the sidebar.")
