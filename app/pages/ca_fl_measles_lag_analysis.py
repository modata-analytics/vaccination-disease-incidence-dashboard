from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import pearsonr

st.set_page_config(page_title="CA & FL Disease Lag Analysis", page_icon="📈", layout="wide")
st.title("California & Florida: Vaccination Coverage & Disease Incidence")
st.write(
    "Explore Pearson correlations between vaccination coverage and subsequent "
    "disease incidence for **California and Florida only**. "
    "Each lag compares coverage in year t − lag with incidence in year t. "
    "These associations do not establish causation."
)

PAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PAGE_DIR.parent / "data" if PAGE_DIR.name == "pages" else PAGE_DIR / "data"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_DIR / "cases_coverage_ms.csv")

try:
    raw = load_data()
except (OSError, pd.errors.ParserError) as exc:
    st.error(f"Unable to load {DATA_DIR / 'cases_coverage_ms.csv'}: {exc}")
    st.stop()

st.sidebar.header("Analysis Filters")
disease = st.sidebar.selectbox("Disease", ["Measles", "Mumps", "Pertussis"])
key = disease.lower()
coverage_col = f"{key}_coverage_pct"
cases_col = f"{key}_cases"
incidence_col = f"{key}_cases_per_100k"

start_year, end_year = st.sidebar.slider(
    "Incidence year range", min_value=1995, max_value=2017, value=(1995, 2017)
)
selected_states = st.sidebar.multiselect(
    "States to display", ["CA", "FL"], default=["CA", "FL"],
    format_func=lambda s: {"CA": "California", "FL": "Florida"}[s],
)

required = {"year", "state", coverage_col}
missing = required - set(raw.columns)
if missing:
    st.error(f"Missing required columns: {', '.join(sorted(missing))}")
    st.stop()

data = raw.loc[raw["state"].isin(["CA", "FL"])].copy()
data["year"] = pd.to_numeric(data["year"], errors="coerce")
data[coverage_col] = pd.to_numeric(data[coverage_col], errors="coerce")
if incidence_col in data.columns:
    data["incidence_per_100k"] = pd.to_numeric(data[incidence_col], errors="coerce")
elif {cases_col, "population"}.issubset(data.columns):
    cases = pd.to_numeric(data[cases_col], errors="coerce")
    population = pd.to_numeric(data["population"], errors="coerce")
    data["incidence_per_100k"] = cases / population.where(population > 0) * 100_000
else:
    st.error(
        f"Need either '{incidence_col}' or both '{cases_col}' and 'population' "
        "to calculate incidence per 100,000."
    )
    st.stop()

data = data.dropna(subset=["year"]).copy()
data["year"] = data["year"].astype(int)
if data.duplicated(["state", "year"]).any():
    st.error("The dataset has duplicate state/year rows. Aggregate these before lag analysis.")
    st.stop()

colors = {"CA": "#3366CC", "FL": "#E67E22"}
names = {"CA": "California", "FL": "Florida"}

def calculate_lags(df):
    rows, pairs = [], {}
    for state in ["CA", "FL"]:
        state_df = df[df["state"] == state]
        coverage = state_df[["year", coverage_col]].rename(columns={"year": "coverage_year"})
        incidence = state_df[["year", "incidence_per_100k"]].rename(
            columns={"year": "incidence_year"}
        )
        for lag in range(6):
            shifted = incidence.copy()
            shifted["coverage_year"] = shifted["incidence_year"] - lag
            matched = coverage.merge(shifted, on="coverage_year", how="inner")
            matched = matched[
                matched["incidence_year"].between(start_year, end_year)
            ].dropna(subset=[coverage_col, "incidence_per_100k"])
            pairs[(state, lag)] = matched
            n = len(matched)
            if n >= 3 and matched[coverage_col].nunique() > 1 and matched["incidence_per_100k"].nunique() > 1:
                r, p = pearsonr(matched[coverage_col], matched["incidence_per_100k"])
            else:
                r, p = np.nan, np.nan
            rows.append({
                "state": state, "lag_years": lag, "n": n,
                "pearson_r": r, "p_value": p,
                "significant_0_05": bool(p < 0.05) if pd.notna(p) else False,
            })
    return pd.DataFrame(rows), pairs

results, pairs = calculate_lags(data)
results = results[results["state"].isin(selected_states)]

st.subheader(f"{disease} Coverage vs Incidence")
st.caption(
    "Each point represents a matched coverage year and incidence year. "
    "Dashed lines show separate linear fits for California and Florida."
)
for lag in range(6):
    fig = go.Figure()
    for state in selected_states:
        matched = pairs[(state, lag)]
        fig.add_trace(go.Scatter(
            x=matched[coverage_col], y=matched["incidence_per_100k"],
            mode="markers", name=names[state],
            marker=dict(color=colors[state], size=9),
            customdata=matched[["coverage_year", "incidence_year"]].to_numpy(),
            hovertemplate=(
                "Coverage year: %{customdata[0]}<br>"
                "Incidence year: %{customdata[1]}<br>"
                "Coverage: %{x:.2f}%<br>"
                "Incidence: %{y:.3f} per 100K<extra></extra>"
            ),
        ))
        if (
            len(matched) >= 3
            and matched[coverage_col].nunique() > 1
            and matched["incidence_per_100k"].nunique() > 1
        ):
            x = matched[coverage_col].to_numpy(dtype=float)
            y = matched["incidence_per_100k"].to_numpy(dtype=float)
            slope, intercept = np.polyfit(x, y, 1)
            xs = np.linspace(x.min(), x.max(), 100)
            fig.add_trace(go.Scatter(
                x=xs, y=slope * xs + intercept, mode="lines",
                line=dict(color=colors[state], dash="dash"),
                name=f"{names[state]} trend", hoverinfo="skip",
            ))
    fig.update_layout(
        title=f"{disease} Coverage vs Incidence — {lag}-Year Lag",
        xaxis_title=f"{disease} vaccination coverage (%)",
        yaxis_title=f"{disease} incidence (cases per 100,000)",
        height=430,
    )
    st.plotly_chart(fig, width="stretch", key=f"{key}_lag_{lag}")

st.subheader(f"{disease}: Pearson Correlation Summary (0–5 Year Lags)")
st.dataframe(
    results.style.format({"pearson_r": "{:.4f}", "p_value": "{:.4g}"}, na_rep="—"),
    width="stretch", hide_index=True,
)

st.caption(
    "Incidence is expressed as reported cases per 100,000 residents. "
    "Correlations are computed independently by state. "
    "The year range filters incidence years; nonzero lags may use earlier coverage years."
)