import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Measles, Mumps, Pertussis Cases & Coverage Notebook",
    layout="wide"
)

st.title("Measles, Mumps, Pertussis Cases & Coverage Notebook")

html_path = Path("app/static/04_rmmp_cases_and_coverage.html")

st.iframe(
    html_path,
    height=1200,
    width="stretch"
)