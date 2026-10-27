import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Analysis Engine for Time Lagged Association",
    layout="wide"
)

st.title("Analysis Engine for Time Lagged Association")

html_path = Path("app/static/analysis_engine.html")

st.iframe(
    html_path,
    height=1200,
    width="stretch"
)