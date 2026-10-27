import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Tycho Measles Control Notebook",
    layout="wide"
)

st.title("Tycho Measles Control Notebook")

html_path = Path("app/static/02_v1.0_tycho_measles_control.html")

st.iframe(
    html_path,
    height=1200,
    width="stretch"
)