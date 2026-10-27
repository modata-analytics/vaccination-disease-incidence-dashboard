import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Getting Missing Cases from MMWR/NNDSS",
    layout="wide"
)

st.title("Getting Missing Cases from MMWR/NNDSS")

html_path = Path("app/static/09_missing_years_cases.html")

st.iframe(
    html_path,
    height=1200,
    width="stretch"
)