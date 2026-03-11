import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import apply_styles, page_header

apply_styles()
page_header("Database Management",
            "Save, reload, and export portfolios and model snapshots within the current session.")

# ── session-state defaults ────────────────────────────────────────────────────
for key, val in [
    ("saved_portfolios", {}),
    ("saved_model_snapshots", {}),
    ("models_trained", False),
    ("model_results", {}),
    ("financial_data", None),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── save current session ──────────────────────────────────────────────────────
st.markdown("### Save Current Session")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Save Portfolio Data**")
    portfolio_name = st.text_input("Portfolio name", value=f"Portfolio_{datetime.now().strftime('%Y%m%d_%H%M')}")
    if st.button("Save Portfolio", disabled=st.session_state.financial_data is None):
        if st.session_state.financial_data is not None:
            st.session_state.saved_portfolios[portfolio_name] = {
                "data":      st.session_state.financial_data.to_dict("records"),
                "saved_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rows":      len(st.session_state.financial_data),
                "columns":   list(st.session_state.financial_data.columns),
            }
            st.success(f"Portfolio '{portfolio_name}' saved.")
        else:
            st.warning("No data to save. Upload data first.")

with col2:
    st.markdown("**Save Model Snapshot**")
    snapshot_name = st.text_input("Snapshot name", value=f"Snapshot_{datetime.now().strftime('%Y%m%d_%H%M')}")
    if st.button("Save Model Snapshot", disabled=not st.session_state.models_trained):
        if st.session_state.models_trained and st.session_state.model_results:
            snapshot = {}
            for m, v in st.session_state.model_results.items():
                snapshot[m] = {
                    k: val for k, val in v.items()
                    if k not in ("fpr", "tpr", "cm")   # keep it light
                }
            st.session_state.saved_model_snapshots[snapshot_name] = {
                "results":  snapshot,
                "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "n_models": len(snapshot),
            }
            st.success(f"Snapshot '{snapshot_name}' saved.")
        else:
            st.warning("No trained models to save. Train models first.")

st.markdown("---")

# ── saved portfolios ──────────────────────────────────────────────────────────
st.markdown("### Saved Portfolios")
if not st.session_state.saved_portfolios:
    st.info("No portfolios saved yet.")
else:
    for pname, pdata in list(st.session_state.saved_portfolios.items()):
        with st.expander(f"{pname}  |  {pdata['rows']:,} rows  |  Saved {pdata['saved_at']}"):
            st.markdown(f"**Columns ({len(pdata['columns'])}):** {', '.join(pdata['columns'][:10])}{'…' if len(pdata['columns'])>10 else ''}")
            c1, c2, c3 = st.columns(3)

            with c1:
                # load back
                if st.button(f"Load into session", key=f"load_{pname}"):
                    df_loaded = pd.DataFrame(pdata["data"])
                    st.session_state.financial_data = df_loaded
                    st.session_state.processed_data = df_loaded
                    st.session_state.data_uploaded  = True
                    st.success(f"Loaded '{pname}' into session.")

            with c2:
                # download
                csv = pd.DataFrame(pdata["data"]).to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name=f"{pname}.csv",
                    mime="text/csv",
                    key=f"dl_{pname}",
                )

            with c3:
                if st.button("Delete", key=f"del_{pname}"):
                    del st.session_state.saved_portfolios[pname]
                    st.rerun()

st.markdown("---")

# ── saved model snapshots ─────────────────────────────────────────────────────
st.markdown("### Saved Model Snapshots")
if not st.session_state.saved_model_snapshots:
    st.info("No model snapshots saved yet.")
else:
    for sname, sdata in list(st.session_state.saved_model_snapshots.items()):
        with st.expander(f"{sname}  |  {sdata['n_models']} model(s)  |  Saved {sdata['saved_at']}"):
            rows = []
            for mname, mv in sdata["results"].items():
                rows.append({
                    "Model":     mname,
                    "AUC":       round(mv.get("auc", 0), 4),
                    "F1":        round(mv.get("f1", 0), 4),
                    "Accuracy":  round(mv.get("accuracy", 0), 4),
                    "ESG":       "Yes" if mv.get("use_esg") else "No",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            c1, c2 = st.columns(2)
            with c1:
                # export as JSON
                json_str = json.dumps(sdata["results"], indent=2)
                st.download_button(
                    "Download Results JSON",
                    data=json_str.encode("utf-8"),
                    file_name=f"{sname}.json",
                    mime="application/json",
                    key=f"jdl_{sname}",
                )
            with c2:
                if st.button("Delete snapshot", key=f"sdel_{sname}"):
                    del st.session_state.saved_model_snapshots[sname]
                    st.rerun()

st.markdown("---")

# ── session overview ──────────────────────────────────────────────────────────
st.markdown("### Current Session Overview")

sc1, sc2, sc3 = st.columns(3)
sc1.metric("Data Loaded",      "Yes" if st.session_state.financial_data is not None else "No")
sc2.metric("Models Trained",   "Yes" if st.session_state.models_trained else "No")
sc3.metric("Saved Portfolios", len(st.session_state.saved_portfolios))

if st.session_state.financial_data is not None:
    df = st.session_state.financial_data
    st.markdown(
        f"**Active dataset:** {len(df):,} rows × {df.shape[1]} columns  "
        f"| Default rate: {df['default_risk'].mean()*100:.1f}%" if "default_risk" in df.columns
        else f"**Active dataset:** {len(df):,} rows × {df.shape[1]} columns"
    )

if st.session_state.models_trained:
    st.markdown(f"**Trained models:** {', '.join(st.session_state.model_results.keys())}")

# ── clear session ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Reset Session")
if st.button("Reset Entire Session", type="secondary"):
    for key in ["data_uploaded", "models_trained", "financial_data",
                "processed_data", "models", "model_results",
                "feature_cols", "esg_feature_cols", "scaler"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Session reset. Start from the Data Upload page.")
    st.rerun()
