import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Extracting & Calculating Vaccine Coverage from NIS Child",
    layout="wide"
)

st.title("Extracting & Calculating Vaccine Coverage from NIS Child")

html_path = Path("app/static/99_extract_csv_from_nis.html")

st.iframe(
    html_path,
    height=1200,
    width="stretch"
)