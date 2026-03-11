import streamlit as st

st.set_page_config(
    page_title="ClimateRsk AI — Risk Modeling Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

pg = st.navigation(
    [
        st.Page("pages/0_Overview.py",            title="Overview"),
        st.Page("pages/1_Data_Upload.py",         title="Data Upload"),
        st.Page("pages/2_Model_Training.py",      title="Model Training"),
        st.Page("pages/3_Model_Comparison.py",    title="Model Comparison"),
        st.Page("pages/4_Risk_Dashboard.py",      title="Risk Dashboard"),
        st.Page("pages/5_Database_Management.py", title="Database Management"),
    ],
    position="sidebar",
)
pg.run()

