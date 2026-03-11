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
page_header("Model Comparison",
            "Evaluate all trained models side-by-side and quantify the ESG performance lift.")

# ── session-state defaults ────────────────────────────────────────────────────
for key, val in [("models_trained", False), ("model_results", {})]:
    if key not in st.session_state:
        st.session_state[key] = val

if not st.session_state.models_trained or not st.session_state.model_results:
    st.warning("No trained models found — please complete Model Training first.")
    st.stop()

results = st.session_state.model_results
METRICS = ["auc", "cv_auc", "accuracy", "precision", "recall", "f1"]
METRIC_LABELS = {
    "auc":       "AUC",
    "cv_auc":    "CV AUC (5-fold)",
    "accuracy":  "Accuracy",
    "precision": "Precision",
    "recall":    "Recall",
    "f1":        "F1 Score",
}

# ── summary table ─────────────────────────────────────────────────────────────
st.markdown("### Performance Summary")
rows = []
for model, v in results.items():
    row = {"Model": model, "ESG": "Yes" if v["use_esg"] else "No"}
    for m in METRICS:
        row[METRIC_LABELS[m]] = round(v[m], 4)
    rows.append(row)
summary_df = pd.DataFrame(rows)

# highlight best per metric
def highlight_max(s):
    is_max = s == s.max()
    return ["background-color: #d4edda; font-weight:bold" if v else "" for v in is_max]

styled = summary_df.style.apply(
    highlight_max, subset=[METRIC_LABELS[m] for m in METRICS]
).set_properties(**{"font-size": "0.88rem"})
st.dataframe(styled, use_container_width=True, hide_index=True)

# ── ESG lift analysis ─────────────────────────────────────────────────────────
st.markdown("### ESG Performance Lift")
baseline = {m: v for m, v in results.items() if not v["use_esg"]}
esg_mdls  = {m: v for m, v in results.items() if v["use_esg"]}

if baseline and esg_mdls:
    lift_rows = []
    for b_name, b_val in baseline.items():
        # find matching ESG version (same algorithm family)
        algo = b_name.replace(" (baseline)", "").strip()
        match = next(
            (n for n in esg_mdls if algo in n), None
        )
        if match:
            e_val = esg_mdls[match]
            lift_rows.append({
                "Baseline Model": b_name,
                "ESG Model":      match,
                "AUC Lift":       round(e_val["auc"]      - b_val["auc"],      4),
                "F1 Lift":        round(e_val["f1"]       - b_val["f1"],       4),
                "Recall Lift":    round(e_val["recall"]   - b_val["recall"],   4),
                "Accuracy Lift":  round(e_val["accuracy"] - b_val["accuracy"], 4),
            })
    if lift_rows:
        lift_df = pd.DataFrame(lift_rows)

        def color_lift(val):
            if isinstance(val, float):
                color = "#2ecc71" if val > 0 else ("#e74c3c" if val < 0 else "")
                return f"color: {color}; font-weight:bold" if color else ""
            return ""

        st.dataframe(
            lift_df.style.applymap(
                color_lift,
                subset=["AUC Lift", "F1 Lift", "Recall Lift", "Accuracy Lift"]
            ),
            use_container_width=True, hide_index=True,
        )
    else:
        st.info("No matching baseline/ESG pairs found for lift analysis.")
else:
    st.info("Train both baseline and ESG versions of a model to see lift analysis.")

# ── bar chart comparison ───────────────────────────────────────────────────────
st.markdown("### Metric Comparison Chart")
sel_metric = st.selectbox("Select metric", list(METRIC_LABELS.values()),
                          index=0)
inv_labels = {v: k for k, v in METRIC_LABELS.items()}
metric_key = inv_labels[sel_metric]

model_names = list(results.keys())
values      = [results[m][metric_key] for m in model_names]
colors      = ["#10b981" if results[m]["use_esg"] else "#3b82f6" for m in model_names]

fig, ax = plt.subplots(figsize=(10, 4), facecolor="#f8fafc")
ax.set_facecolor("#f8fafc")
bars = ax.bar(model_names, values, color=colors, edgecolor="white", linewidth=0.5)
ax.bar_label(bars, fmt="%.4f", padding=3, fontsize=9)
ax.set_ylim(0, min(1.05, max(values) * 1.15))
ax.set_ylabel(sel_metric, fontsize=10)
ax.set_title(f"{sel_metric} — All Models", fontsize=12, fontweight="bold", color="#0f172a")
plt.xticks(rotation=20, ha="right", fontsize=9)
ax.grid(axis="y", alpha=0.2, color="#e2e8f0")
ax.spines[["top","right"]].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[
    Patch(color="#10b981", label="With ESG"),
    Patch(color="#3b82f6", label="Without ESG"),
])
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ── ROC overlay ───────────────────────────────────────────────────────────────
st.markdown("### ROC Curve Comparison")
fig2, ax2 = plt.subplots(figsize=(8, 5), facecolor="#f8fafc")
ax2.set_facecolor("#f8fafc")
ax2.plot([0, 1], [0, 1], color="#cbd5e1", lw=1.5, ls="--", label="Random baseline")
for m, v in results.items():
    ls = "-" if v["use_esg"] else "--"
    ax2.plot(v["fpr"], v["tpr"],
             linestyle=ls, lw=2,
             label=f"{m} (AUC={v['auc']:.3f})")
ax2.set_xlabel("False Positive Rate", fontsize=10)
ax2.set_ylabel("True Positive Rate", fontsize=10)
ax2.set_title("ROC Curves  (solid = with ESG, dashed = without)",
              fontsize=12, fontweight="bold", color="#0f172a")
ax2.legend(fontsize=8, loc="lower right", framealpha=0.9)
ax2.grid(alpha=0.2, color="#e2e8f0")
ax2.spines[["top","right"]].set_visible(False)
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# ── confusion matrices ────────────────────────────────────────────────────────
st.markdown("### Confusion Matrices")
cols = st.columns(min(len(results), 3))
for idx, (m, v) in enumerate(results.items()):
    with cols[idx % 3]:
        cm = np.array(v["cm"])
        fig3, ax3 = plt.subplots(figsize=(3, 3))
        im = ax3.imshow(cm, cmap="Blues")
        ax3.set_xticks([0, 1]); ax3.set_yticks([0, 1])
        ax3.set_xticklabels(["Pred 0", "Pred 1"], fontsize=8)
        ax3.set_yticklabels(["Act 0", "Act 1"],   fontsize=8)
        for i in range(2):
            for j in range(2):
                ax3.text(j, i, str(cm[i, j]),
                         ha="center", va="center",
                         color="white" if cm[i, j] > cm.max() / 2 else "black",
                         fontsize=12, fontweight="bold")
        ax3.set_title(m[:30], fontsize=7)
        plt.colorbar(im, ax=ax3, fraction=0.046)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

# ── feature importance comparison ─────────────────────────────────────────────
tree_results = {m: v for m, v in results.items() if v["feature_importances"]}
if len(tree_results) >= 2:
    st.markdown("### Feature Importance Comparison")
    fi_compare = {}
    for m, v in tree_results.items():
        for feat, imp in v["feature_importances"].items():
            fi_compare.setdefault(feat, {})[m] = imp
    fi_df = pd.DataFrame(fi_compare).T.fillna(0)
    fi_df["max_imp"] = fi_df.max(axis=1)
    fi_df = fi_df.sort_values("max_imp", ascending=False).head(15).drop(columns="max_imp")

    fig4, ax4 = plt.subplots(figsize=(10, 5), facecolor="#f8fafc")
    ax4.set_facecolor("#f8fafc")
    x = np.arange(len(fi_df))
    width = 0.8 / len(fi_df.columns)
    for i, col in enumerate(fi_df.columns):
        cval = "#10b981" if results.get(col, {}).get("use_esg") else "#3b82f6"
        ax4.bar(x + i * width, fi_df[col], width, label=col[:25], color=cval, alpha=0.85)
    ax4.set_xticks(x + width * len(fi_df.columns) / 2)
    ax4.set_xticklabels(fi_df.index, rotation=35, ha="right", fontsize=8)
    ax4.set_ylabel("Importance", fontsize=10)
    ax4.set_title("Top-15 Feature Importances", fontsize=12, fontweight="bold", color="#0f172a")
    ax4.legend(fontsize=7)
    ax4.grid(axis="y", alpha=0.2, color="#e2e8f0")
    ax4.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)
