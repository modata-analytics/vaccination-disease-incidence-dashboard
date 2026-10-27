import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Lag Phase Analysis",
    layout="wide"
)

st.title("Lag Phase Analysis")

html_path = Path("app/static/lag_phase_analysis.html")

st.iframe(
    html_path,
    height=1200,
    width="stretch"
)