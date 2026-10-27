import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pearsonr
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Time-Lagged Association by State", page_icon="⏳", layout="wide")

MASTER_CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "cases_coverage_ms.csv"
DISEASES = ("measles", "mumps", "pertussis")


@st.cache_data
def load_master(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    required = {"state", "year"}
    for disease in DISEASES:
        required.add(f"{disease}_coverage_pct")
        incidence = f"{disease}_cases_per_100k"
        if incidence not in data.columns:
            if f"{disease}_cases" not in data.columns or "population" not in data.columns:
                raise ValueError(
                    f"Missing {incidence}; provide that column or both "
                    f"{disease}_cases and population."
                )
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    data = data.copy()
    data["year"] = pd.to_numeric(data["year"], errors="coerce")
    data = data.dropna(subset=["state", "year"])
    data["year"] = data["year"].astype(int)
    data["state"] = data["state"].astype(str).str.strip()
    for disease in DISEASES:
        coverage = f"{disease}_coverage_pct"
        incidence = f"{disease}_cases_per_100k"
        data[coverage] = pd.to_numeric(data[coverage], errors="coerce")
        if incidence not in data.columns:
            cases = pd.to_numeric(data[f"{disease}_cases"], errors="coerce")
            population = pd.to_numeric(data["population"], errors="coerce")
            data[incidence] = cases / population.where(population > 0) * 100_000
        else:
            data[incidence] = pd.to_numeric(data[incidence], errors="coerce")
    if data.duplicated(["state", "year"]).any():
        raise ValueError("Master CSV has duplicate state-year rows; expected one row per state and year.")
    return data.sort_values(["state", "year"]).reset_index(drop=True)


def pearson_lag_analysis(df, state, disease, start_year, end_year, max_lag=5):
    """Use identical coverage years for every lag from 1 through max_lag."""
    coverage_col = f"{disease}_coverage_pct"
    incidence_col = f"{disease}_cases_per_100k"
    data = df.loc[
        (df["state"] == state) & df["year"].between(start_year, end_year),
        ["year", coverage_col, incidence_col],
    ].sort_values("year").copy()
    if data["year"].duplicated().any():
        raise ValueError("Duplicate years found for the selected state.")
    data = data.set_index("year")
    valid_years = []
    for year in data.index:
        if not np.isfinite(data.at[year, coverage_col]):
            continue
        if all(
            (year + lag in data.index)
            and np.isfinite(data.at[year + lag, incidence_col])
            for lag in range(1, max_lag + 1)
        ):
            valid_years.append(year)

    results = []
    for lag in range(1, max_lag + 1):
        x = np.array([data.at[year, coverage_col] for year in valid_years], dtype=float)
        y = np.array([data.at[year + lag, incidence_col] for year in valid_years], dtype=float)
        n = len(x)
        if n >= 3 and np.ptp(x) > 0 and np.ptp(y) > 0:
            r, p = pearsonr(x, y)
        else:
            r, p = np.nan, np.nan
        results.append({
            "state": state,
            "disease": disease,
            "start_year": start_year,
            "end_year": end_year,
            "lag_years": lag,
            "n": n,
            "pearson_r": r,
            "p_value": p,
            "significant_0_05": bool(p < 0.05) if np.isfinite(p) else False,
        })
    return pd.DataFrame(results), valid_years


def graph_coverage_cases_lag(df, results, disease, state):
    plot = results.sort_values("lag_years").copy()
    # Display convention: lag k is positioned at start_year + k.
    # Correlations are calculated across many paired years, not at one calendar year.
    plot["display_year"] = plot["start_year"] + plot["lag_years"]

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
        subplot_titles=[
            "Vaccination Coverage & Disease Incidence",
            "Pearson Correlation by Lag Duration",
        ],
        vertical_spacing=0.12,
        row_heights=[0.55, 0.45],
    )
    fig.add_trace(
        go.Bar(
            x=df["year"],
            y=df[f"{disease}_cases_per_100k"],
            name="Cases per 100K",
            marker_color="#E74C3C",
            opacity=0.65,
            hovertemplate="Year: %{x}<br>Cases per 100K: %{y:.3f}<extra></extra>",
        ),
        row=1, col=1, secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df[f"{disease}_coverage_pct"],
            name="Vaccination coverage",
            mode="lines+markers",
            line=dict(color="#3498DB", width=2),
            hovertemplate="Year: %{x}<br>Coverage: %{y:.2f}%<extra></extra>",
        ),
        row=1, col=1, secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            x=plot["display_year"],
            y=plot["pearson_r"],
            mode="lines+markers",
            name="Pearson r",
            line=dict(color="#3498DB", width=2),
            marker=dict(
                size=11,
                color=["#2ECC71" if significant else "#3498DB"
                       for significant in plot["significant_0_05"]],
                line=dict(color="white", width=1),
            ),
            customdata=plot[["lag_years", "n", "p_value"]].to_numpy(),
            hovertemplate=(
                "Displayed year: %{x}<br>Lag: %{customdata[0]:.0f} years<br>"
                "Pearson r: %{y:.3f}<br>n: %{customdata[1]:.0f}<br>"
                "Unadjusted p-value: %{customdata[2]:.4g}<extra></extra>"
            ),
        ),
        row=2, col=1,
    )
    fig.update_yaxes(title_text="Cases per 100K", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Vaccination Coverage (%)", row=1, col=1, secondary_y=True)
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_xaxes(
        title_text="Calendar year (lag aligned to starting year)",
        range=[df["year"].min() - 0.5, df["year"].max() + 0.5],
        dtick=1,
        row=2, col=1,
    )
    fig.update_yaxes(
        title_text="Pearson Correlation (r)", range=[-1, 1],
        zeroline=False, row=2, col=1,
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
    fig.update_layout(
        title=f"{state} — {disease.title()} Vaccination Coverage, Incidence & Lag Analysis",
        template="plotly_white",
        height=850,
        hovermode="closest",
        legend=dict(orientation="h", y=1.07, x=0),
        margin=dict(t=120, b=60),
    )
    return fig


st.title("⏳ Time-Lagged Association: Vaccine Coverage & Disease Incidence")
st.sidebar.header("Time-Lagged Association by State")
st.write("""
### State-Level Analysis
Explore whether vaccination coverage in a given year is associated with disease
incidence in later years. Select a state, disease, year range, and maximum lag.
The incidence measure is **cases per 100,000 population**. The Pearson analysis
uses the **same coverage years for every lag**, so changing the maximum lag may
also change the correlations at shorter lags.

A negative correlation means higher coverage years tended to precede lower
incidence; a positive correlation means higher coverage years tended to precede
higher incidence. **Neither direction establishes causation.**
""")

try:
    master_df = load_master(MASTER_CSV_PATH)
except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Unable to load master CSV at `{MASTER_CSV_PATH}`: {exc}")
    st.stop()

state = st.selectbox("Select state", sorted(master_df["state"].dropna().unique()))
disease = st.selectbox("Select disease", DISEASES, format_func=str.title)
state_df = master_df.loc[master_df["state"] == state].copy()
min_year, max_year = int(state_df["year"].min()), int(state_df["year"].max())
if min_year == max_year:
    st.warning("Only one year is available for this state; lag analysis requires multiple years.")
    st.stop()

start_year, end_year = st.slider(
    "Select analysis years", min_value=min_year, max_value=max_year,
    value=(min_year, max_year), step=1,
)
window_length = end_year - start_year
if window_length < 1:
    st.warning("Select at least two different years to examine time lags.")
    st.stop()

max_lag = st.slider(
    "Maximum lag (years)", min_value=1,
    max_value=min(10, window_length), value=min(5, window_length), step=1,
)
filtered_df = state_df.loc[state_df["year"].between(start_year, end_year)].copy()

results, valid_years = pearson_lag_analysis(
    df=master_df, state=state, disease=disease,
    start_year=start_year, end_year=end_year, max_lag=max_lag,
)

st.subheader("Vaccination Coverage & Time-Lagged Association")
st.plotly_chart(
    graph_coverage_cases_lag(filtered_df, results, disease, state),
    width="stretch",
)
st.caption(
    "For visual alignment, the lag-k correlation is displayed at starting year + k. "
    "Each correlation summarizes multiple annual pairs, not a single calendar year."
)

if results["pearson_r"].notna().any():
    st.caption(
        f"Common coverage-year window: {min(valid_years)}–{max(valid_years)} "
        f"({len(valid_years)} valid year pairs per lag). "
        "Incidence years shift forward by the selected lag."
    )
else:
    st.warning(
        "Insufficient non-missing, non-constant observations for a Pearson "
        "correlation with the selected years and maximum lag. "
        "Try a wider year range or a shorter maximum lag."
    )

st.dataframe(results, hide_index=True, width="stretch")
st.caption(
    "Green markers indicate unadjusted p < 0.05; blue markers do not. "
    "These p-values are exploratory and are not adjusted for multiple lag "
    "tests, temporal autocorrelation, shared trends, or confounding. "
    "NIS coverage concerns young children, whereas reported cases are not "
    "age-matched to those children."
)