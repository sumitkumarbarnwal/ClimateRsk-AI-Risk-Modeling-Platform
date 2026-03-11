import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import apply_styles, page_header

apply_styles()
page_header("Risk Dashboard",
            "Explore per-company risk predictions, segment breakdowns, and climate variable impact.")

# ── session-state defaults ────────────────────────────────────────────────────
for key, val in [
    ("models_trained", False),
    ("model_results", {}),
    ("models", {}),
    ("financial_data", None),
    ("processed_data", None),
    ("feature_cols", []),
    ("esg_feature_cols", []),
]:
    if key not in st.session_state:
        st.session_state[key] = val

if not st.session_state.models_trained or not st.session_state.model_results:
    st.warning("No trained models found — please complete Model Training first.")
    st.stop()

results = st.session_state.model_results
models  = st.session_state.models
df      = st.session_state.financial_data.copy()

ESG_COLS = {"esg_score", "carbon_exposure", "green_ratio",
            "climate_risk_idx", "water_stress", "governance_score", "social_score"}

# ── model selector ─────────────────────────────────────────────────────────────
model_names = list(models.keys())
selected_model = st.selectbox("Select model for predictions", model_names,
                              index=len(model_names) - 1)

res      = results[selected_model]
model    = models[selected_model]
feat_cols = res["feat_cols"]

X_all = df[feat_cols].fillna(df[feat_cols].median())
proba = model.predict_proba(X_all)[:, 1]
pred  = model.predict(X_all)

df["risk_probability"] = proba
df["risk_prediction"]  = pred
df["risk_tier"] = pd.cut(
    proba,
    bins=[0, 0.33, 0.66, 1.0],
    labels=["Low", "Medium", "High"]
)

# ── KPI cards ─────────────────────────────────────────────────────────────────
st.markdown("### Portfolio Risk Overview")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Companies",  f"{len(df):,}")
c2.metric("High Risk",        f"{(df['risk_tier']=='High').sum():,}",
          delta=f"{(df['risk_tier']=='High').mean()*100:.1f}%")
c3.metric("Medium Risk",      f"{(df['risk_tier']=='Medium').sum():,}")
c4.metric("Low Risk",         f"{(df['risk_tier']=='Low').sum():,}")
c5.metric("Avg Risk Prob",    f"{proba.mean():.3f}")

# ── risk distribution ─────────────────────────────────────────────────────────
st.markdown("### Risk Distribution")
col_a, col_b = st.columns(2)

with col_a:
    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#f8fafc")
    ax.set_facecolor("#f8fafc")
    ax.hist(proba, bins=40, color="#3b82f6", edgecolor="white", linewidth=0.4)
    ax.axvline(0.33, color="#f59e0b", ls="--", lw=1.5, label="Low/Med threshold")
    ax.axvline(0.66, color="#ef4444", ls="--", lw=1.5, label="Med/High threshold")
    ax.set_xlabel("Risk Probability", fontsize=9)
    ax.set_ylabel("Count", fontsize=9)
    ax.set_title("Risk Probability Distribution", fontsize=11,
                 fontweight="bold", color="#0f172a")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2, color="#e2e8f0")
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col_b:
    tier_counts = df["risk_tier"].value_counts().reindex(["Low", "Medium", "High"])
    colors = ["#10b981", "#f59e0b", "#ef4444"]
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    wedges, texts, autotexts = ax2.pie(
        tier_counts, labels=tier_counts.index,
        autopct="%1.1f%%", colors=colors, startangle=90
    )
    ax2.set_title("Risk Tier Breakdown", fontsize=11, fontweight="bold", color="#0f172a")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# ── sector / region analysis ──────────────────────────────────────────────────
if "sector" in df.columns or "region" in df.columns:
    st.markdown("### Risk by Segment")
    seg_cols = st.columns(2)
    idx = 0
    for seg in ["sector", "region"]:
        if seg not in df.columns:
            continue
        grp = df.groupby(seg)["risk_probability"].agg(["mean", "count"]).reset_index()
        grp.columns = [seg.title(), "Avg Risk", "Count"]
        grp = grp.sort_values("Avg Risk", ascending=False)
        with seg_cols[idx % 2]:
            fig3, ax3 = plt.subplots(figsize=(6, 3.5))
            bar_colors = plt.cm.RdYlGn_r(
                (grp["Avg Risk"] - grp["Avg Risk"].min()) /
                (grp["Avg Risk"].max() - grp["Avg Risk"].min() + 1e-9)
            )
            ax3.barh(grp[seg.title()], grp["Avg Risk"], color=bar_colors)
            ax3.set_xlabel("Average Risk Probability", fontsize=9)
            ax3.set_title(f"Risk by {seg.title()}", fontsize=11,
                         fontweight="bold", color="#0f172a")
            ax3.grid(axis="x", alpha=0.2, color="#e2e8f0")
            ax3.spines[["top","right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)
        idx += 1

# ── ESG vs risk scatter ────────────────────────────────────────────────────────
esg_present = [c for c in ESG_COLS if c in df.columns]
if esg_present:
    st.markdown("### ESG Factors vs Risk Probability")
    esg_sel = st.selectbox("Select ESG indicator", esg_present)
    fig4, ax4 = plt.subplots(figsize=(8, 4), facecolor="#f8fafc")
    ax4.set_facecolor("#f8fafc")
    tier_colors = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}
    for tier, tc in tier_colors.items():
        mask = df["risk_tier"] == tier
        ax4.scatter(df.loc[mask, esg_sel], df.loc[mask, "risk_probability"],
                    alpha=0.4, s=15, c=tc, label=tier)
    # trend line
    z = np.polyfit(df[esg_sel].fillna(0), df["risk_probability"], 1)
    p = np.poly1d(z)
    xs = np.linspace(df[esg_sel].min(), df[esg_sel].max(), 100)
    ax4.plot(xs, p(xs), "k--", lw=1.5, label="Trend")
    ax4.set_xlabel(esg_sel.replace("_", " ").title(), fontsize=10)
    ax4.set_ylabel("Risk Probability", fontsize=10)
    ax4.set_title(f"{esg_sel.replace('_',' ').title()} vs Risk Probability",
                  fontsize=12, fontweight="bold", color="#0f172a")
    ax4.legend(fontsize=9, framealpha=0.9)
    ax4.grid(alpha=0.2, color="#e2e8f0")
    ax4.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

# ── feature importance ────────────────────────────────────────────────────────
if res["feature_importances"]:
    st.markdown("### Climate Variable Importance")
    fi = pd.Series(res["feature_importances"]).sort_values(ascending=False).head(15)
    colors = ["#10b981" if f in ESG_COLS else "#3b82f6" for f in fi.index]
    fig5, ax5 = plt.subplots(figsize=(8, 4), facecolor="#f8fafc")
    ax5.set_facecolor("#f8fafc")
    ax5.barh(fi.index, fi.values, color=colors, height=0.65)
    ax5.invert_yaxis()
    ax5.set_xlabel("Importance", fontsize=10)
    ax5.set_title("Top-15 Features", fontsize=12, fontweight="bold", color="#0f172a")
    ax5.grid(axis="x", alpha=0.2, color="#e2e8f0")
    ax5.spines[["top","right"]].set_visible(False)
    from matplotlib.patches import Patch
    ax5.legend(handles=[
        Patch(color="#10b981", label="ESG / Climate"),
        Patch(color="#3b82f6", label="Financial"),
    ])
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

# ── high-risk companies table ─────────────────────────────────────────────────
st.markdown("### High Risk Companies")
high_risk = df[df["risk_tier"] == "High"].copy()
display_cols = ["risk_probability", "risk_tier"]
for c in ["company_id", "sector", "portfolio_value", "credit_score",
          "esg_score", "carbon_exposure", "default_risk"]:
    if c in high_risk.columns:
        display_cols.insert(0, c)
# deduplicate
seen = set()
display_cols = [c for c in display_cols if not (c in seen or seen.add(c))]
st.dataframe(
    high_risk[display_cols].sort_values("risk_probability", ascending=False).head(50),
    use_container_width=True, hide_index=True,
)

# ── download ──────────────────────────────────────────────────────────────────
st.markdown("### Export Predictions")
export_cols = display_cols.copy()
for c in ["risk_probability", "risk_prediction", "risk_tier"]:
    if c not in export_cols:
        export_cols.append(c)
export_df = df[[c for c in export_cols if c in df.columns]]
csv_data = export_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Predictions as CSV",
    data=csv_data,
    file_name="risk_predictions.csv",
    mime="text/csv",
)
