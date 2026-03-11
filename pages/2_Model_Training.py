import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score, accuracy_score, precision_score,
    recall_score, f1_score, confusion_matrix, roc_curve,
)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import apply_styles, page_header

apply_styles()
page_header("Model Training",
            "Configure and train machine learning models with or without ESG factors.")

# ── session-state defaults ────────────────────────────────────────────────────
for key, val in [
    ("data_uploaded", False),
    ("models_trained", False),
    ("financial_data", None),
    ("processed_data", None),
    ("models", {}),
    ("model_results", {}),
    ("scaler", None),
    ("feature_cols", []),
    ("esg_feature_cols", []),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.data_uploaded or st.session_state.financial_data is None:
    st.warning("No data loaded — please complete the Data Upload step first.")
    st.stop()

df = st.session_state.financial_data.copy()

# ── feature selection ─────────────────────────────────────────────────────────
EXCLUDE = {"company_id", "default_risk", "sector", "region"}
numeric_cols = [c for c in df.select_dtypes(include=np.number).columns if c not in EXCLUDE]

ESG_COLS = {"esg_score", "carbon_exposure", "green_ratio",
            "climate_risk_idx", "water_stress", "governance_score", "social_score"}
base_cols = [c for c in numeric_cols if c not in ESG_COLS]
esg_cols  = [c for c in numeric_cols if c in ESG_COLS]

st.markdown("### Training Configuration")
col1, col2 = st.columns(2)

with col1:
    test_size  = st.slider("Test set size (%)", 10, 40, 20) / 100
    n_estimators = st.slider("Number of trees / estimators", 50, 500, 100, 50)

with col2:
    max_depth  = st.slider("Max depth", 2, 20, 5)
    random_state = st.number_input("Random seed", value=42, step=1)

selected_models = st.multiselect(
    "Select models to train",
    ["Random Forest (baseline)", "Gradient Boosting (baseline)",
     "Random Forest + ESG",      "Gradient Boosting + ESG",
     "Logistic Regression (baseline)", "Logistic Regression + ESG"],
    default=["Random Forest (baseline)", "Random Forest + ESG",
             "Gradient Boosting + ESG"],
)

st.markdown("---")

# ── training ──────────────────────────────────────────────────────────────────
if st.button("Train Selected Models", type="primary", disabled=len(selected_models) == 0):
    if "default_risk" not in df.columns:
        st.error("Target column `default_risk` not found in data.")
        st.stop()

    # drop rows with NaN in numeric cols
    df_clean = df[numeric_cols + ["default_risk"]].dropna()
    y = df_clean["default_risk"]

    results = {}
    trained_models = {}
    scaler = StandardScaler()

    progress = st.progress(0)
    status   = st.empty()

    for idx, model_name in enumerate(selected_models):
        status.text(f"Training: {model_name} ...")
        progress.progress((idx) / len(selected_models))

        use_esg = "+ ESG" in model_name
        feat_cols = base_cols + (esg_cols if use_esg else [])
        feat_cols = [c for c in feat_cols if c in df_clean.columns]

        X = df_clean[feat_cols]
        X_scaled = scaler.fit_transform(X) if "Logistic" in model_name else X.values

        X_tr, X_te, y_tr, y_te = train_test_split(
            X_scaled, y, test_size=test_size, random_state=int(random_state), stratify=y
        )

        # pick estimator
        if "Random Forest" in model_name:
            clf = RandomForestClassifier(
                n_estimators=n_estimators, max_depth=max_depth,
                random_state=int(random_state), n_jobs=-1
            )
        elif "Gradient Boosting" in model_name:
            clf = GradientBoostingClassifier(
                n_estimators=n_estimators, max_depth=max_depth,
                random_state=int(random_state)
            )
        else:
            clf = LogisticRegression(max_iter=1000, random_state=int(random_state))

        clf.fit(X_tr, y_tr)
        y_pred  = clf.predict(X_te)
        y_proba = clf.predict_proba(X_te)[:, 1]
        cv_auc  = cross_val_score(clf, X_scaled, y, cv=5,
                                  scoring="roc_auc", n_jobs=-1).mean()

        fpr, tpr, _ = roc_curve(y_te, y_proba)
        cm          = confusion_matrix(y_te, y_pred)

        results[model_name] = {
            "accuracy":  accuracy_score(y_te, y_pred),
            "auc":       roc_auc_score(y_te, y_proba),
            "precision": precision_score(y_te, y_pred, zero_division=0),
            "recall":    recall_score(y_te, y_pred, zero_division=0),
            "f1":        f1_score(y_te, y_pred, zero_division=0),
            "cv_auc":    cv_auc,
            "fpr":       fpr.tolist(),
            "tpr":       tpr.tolist(),
            "cm":        cm.tolist(),
            "feat_cols": feat_cols,
            "use_esg":   use_esg,
            "feature_importances": (
                dict(zip(feat_cols, clf.feature_importances_))
                if hasattr(clf, "feature_importances_") else {}
            ),
        }
        trained_models[model_name] = clf

    progress.progress(1.0)
    status.text("All models trained successfully.")

    st.session_state.models        = trained_models
    st.session_state.model_results = results
    st.session_state.models_trained = True
    st.session_state.scaler         = scaler
    st.session_state.feature_cols   = base_cols
    st.session_state.esg_feature_cols = esg_cols

    st.success(f"Trained {len(selected_models)} model(s) successfully.")

# ── show results ──────────────────────────────────────────────────────────────
if st.session_state.models_trained and st.session_state.model_results:
    results = st.session_state.model_results

    st.markdown("### Training Results")
    summary = pd.DataFrame([
        {
            "Model":     m,
            "AUC":       f"{v['auc']:.4f}",
            "CV AUC":    f"{v['cv_auc']:.4f}",
            "Accuracy":  f"{v['accuracy']:.4f}",
            "Precision": f"{v['precision']:.4f}",
            "Recall":    f"{v['recall']:.4f}",
            "F1":        f"{v['f1']:.4f}",
            "ESG":       "Yes" if v['use_esg'] else "No",
        }
        for m, v in results.items()
    ])
    st.dataframe(summary, use_container_width=True, hide_index=True)

    # ROC curves
    st.markdown("### ROC Curves")
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="#f8fafc")
    ax.set_facecolor("#f8fafc")
    ax.plot([0, 1], [0, 1], color="#cbd5e1", lw=1.5, ls="--", label="Random baseline")
    for m, v in results.items():
        ax.plot(v["fpr"], v["tpr"],
                label=f"{m} (AUC={v['auc']:.3f})", lw=2)
    ax.set_xlabel("False Positive Rate", fontsize=10)
    ax.set_ylabel("True Positive Rate", fontsize=10)
    ax.set_title("ROC Curves", fontsize=12, fontweight="bold", color="#0f172a")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
    ax.grid(alpha=0.2, color="#e2e8f0")
    ax.spines[["top","right"]].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

    # Feature importance for first tree-based model
    tree_models = {m: v for m, v in results.items() if v["feature_importances"]}
    if tree_models:
        best = max(tree_models, key=lambda m: tree_models[m]["auc"])
        fi = tree_models[best]["feature_importances"]
        fi_df = pd.DataFrame(
            {"Feature": list(fi.keys()), "Importance": list(fi.values())}
        ).sort_values("Importance", ascending=False).head(15)

        st.markdown(f"### Feature Importance — {best}")
        fig2, ax2 = plt.subplots(figsize=(8, 5), facecolor="#f8fafc")
        ax2.set_facecolor("#f8fafc")
        colors = ["#10b981" if f in ESG_COLS else "#3b82f6" for f in fi_df["Feature"]]
        ax2.barh(fi_df["Feature"], fi_df["Importance"], color=colors, height=0.65)
        ax2.set_xlabel("Importance", fontsize=10)
        ax2.invert_yaxis()
        ax2.grid(axis="x", alpha=0.2, color="#e2e8f0")
        ax2.spines[["top","right"]].set_visible(False)
        ax2.set_title("Feature Importance", fontsize=12, fontweight="bold", color="#0f172a")
        from matplotlib.patches import Patch
        ax2.legend(handles=[
            Patch(color="#10b981", label="ESG / Climate"),
            Patch(color="#3b82f6", label="Financial"),
        ])
        st.pyplot(fig2)
        plt.close(fig2)

    st.success("Models trained — proceed to Model Comparison or Risk Dashboard.")
